import numpy as np
from scipy.signal import convolve2d

import os
import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)
from netpbm import netpbm
from log import write_log, collapse_log

# This code was provided by Dan Torop for ART 3699
COUNT_NEIGHBORS = np.array([[1,1,1],
                            [1,0,1],
                            [1,1,1]])

def conway(image:netpbm.Netpbm) -> netpbm.Netpbm:
    """Return image after one iteration of Conway's Game of Life.

    Args:
        image (np.ndarray): Current world state of Conway's Game of Life.

    Returns:
        np.ndarray: Current world state one iteration in the future.
    """
    M = image.M

    # This code was provided by Dan Torop for ART 3699
    neighbors = convolve2d(M, COUNT_NEIGHBORS, mode="same", boundary="wrap")
    survive = M & ((neighbors == 2) | (neighbors == 3))
    born = neighbors == 3
    M = survive | born

    return netpbm.Netpbm(P=image.P, w=image.w, h=image.h, k=image.k, M=M)

# COMPILE PIECES | 2021-04-07

pieces = [('beebe_trail', 100),
          ('water_cup', 2000)]

logs = []
for name, g in pieces:
    # generate first iteration
    if not os.path.isdir("%s/%s" % (SOURCE_DIR, name)):
        os.mkdir("%s/%s" % (SOURCE_DIR, name))
    file_path = "%s/%s/%s_conway_%s.pbm" % (SOURCE_DIR, name,
                                                name, str(1).zfill(4))
    ppm_path = '%s/%s.ppm' % (SOURCE_DIR, name)
    netpbm.transform(in_path=ppm_path, out_path=file_path,
                     magic_number=1, f=(lambda image : image))

    # generate remaining iterations
    for k in range(2,g):
        in_path = "%s/%s/%s_conway_%s.pbm" % (SOURCE_DIR, name,
                                              name, str(k-1).zfill(4))
        out_path = "%s/%s/%s_conway_%s.pbm" % (SOURCE_DIR, name,
                                               name, str(k).zfill(4))
        M = netpbm.read(in_path)
        M = conway(M)
        netpbm.write(out_path, M)

    log = netpbm.animate("%s/%s/%s_conway_%%04d.pbm" % (SOURCE_DIR, name, name),
                         "%s/%s_conway_animation.mp4" % (SOURCE_DIR, name),
                         fps=30)
    logs.append(log)

write_log('%s/%s' % (SOURCE_DIR, 'conway.log'), logs)
