import numpy as np
from scipy.signal import convolve2d

import os
import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)
from netpbm import netpbm
from animation.animation import animation
from log import write_log

# This code was provided by Dan Torop for ART 3699
COUNT_NEIGHBORS = np.array([[1,1,1],
                            [1,0,1],
                            [1,1,1]])


def conway(M:np.ndarray) -> np.ndarray:
    """Return image after one iteration of Conway's Game of Life.

    Args:
        image (np.ndarray): Current world state of Conway's Game of Life.

    Returns:
        np.ndarray: Current world state one iteration in the future.
    """
    # This code was provided by Dan Torop for ART 3699
    neighbors = convolve2d(M, COUNT_NEIGHBORS, mode="same", boundary="wrap")
    survive = M & ((neighbors == 2) | (neighbors == 3))
    born = neighbors == 3
    return survive | born


# COMPILE PIECES | 2021-04-07

pieces = [('beebe_trail', 100),
          ('water_cup', 2000)]

log = []
for name, g in pieces:
    path = '%s/%s.ppm' % (SOURCE_DIR, name)
    M = netpbm.read(netpbm.raw_to_plain(path, magic_number=1)).M
    frames = [conway(M)]
    for i in range(g):
        frames.append(conway(frames[-1]))
    frames = [np.where(f == 1,0,255) for f in frames]
    file_name = '%s/%s_conway_animation.mp4' % (SOURCE_DIR, name)
    log.append(animation(frames=frames, path=file_name, fps=30, s=4))

write_log('%s/%s' % (SOURCE_DIR, 'conway.log'), log)
