import os
import time
import numpy as np
from math import ceil

import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)
from netpbm import netpbm
from log import write_log, collapse_log


def partition(image:netpbm.Netpbm, k:int, b:int) -> netpbm.Netpbm:
    """Return the Netpbm image mod k.

    Args:
        image (netpbm.Netpbm): Netpbm image to mod.
        k (int): Number of gradients.
        b (int): Width of the border in pixels.

    Returns:
        netpbm.Netpbm: NumPy matrix representing the mod image.
    """
    image = netpbm.change_gradient(image, k)
    h,w = image.M.shape
    layers = []
    for i in range(k):
        M = np.where(image.M == i,k,0)
        layers.append(netpbm.Netpbm(w=w, h=h, k=k, M=M))
    for i in range(k):
        M = np.where(image.M == i,0,k)
        layers.append(netpbm.Netpbm(w=w, h=h, k=k, M=M))
    for i in range(k):
        M = np.where(image.M == i,i,0)
        layers.append(netpbm.Netpbm(w=w, h=h, k=k, M=M))
    for i in range(k):
        M = np.where(image.M == i,0,i)
        layers.append(netpbm.Netpbm(w=w, h=h, k=k, M=M))
    return netpbm.image_grid(layers,k,4,b)


# COMPILE PIECES | 2021-03-20

# single prints

pieces = [('road_day', 8, 30),
          ('sky', 8, 30),
          ('tree', 8, 30),
          ('beebe_day', 8, 30),
          ('waterfall', 8, 30),
          ('risley', 8, 30),
          ('creek', 8, 30),
          ('fallen_tree', 8, 30),
          ('old_man', 8, 30),
          ('wading', 8, 30),
          ('island', 8, 30)]

log = []
for name, k, b in pieces:
    file_path = "%s/%s_partition_%d.pgm" % (SOURCE_DIR, name, k)
    ppm_path = '%s/%s.ppm' % (SOURCE_DIR, name)
    file_log = netpbm.transform(in_path=ppm_path, out_path=file_path,
                                magic_number=2, f=partition, k=k, b=b,
                                scale=2000)
    log.append(file_log)

write_log('%s/%s' % (SOURCE_DIR, 'partition.log'), log)
