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


def clip(image:netpbm.Netpbm,
         k:int, lb:int, ub:int, b:int, c:str) -> netpbm.Netpbm:
    """Return the Netpbm image mod k.

    Args:
        image (netpbm.Netpbm): Netpbm image to mod.
        k (int): Number of gradients.
        lb (int): Lower bound of gradients to show.
        ub (int): Upper bound of gradients to show.
        b (int): Width of the border.
        c (str): Color of the border {'white', 'black'}

    Returns:
        netpbm.Netpbm: NumPy matrix representing the mod image.
    """
    image = netpbm.change_gradient(image, k)
    h,w = image.M.shape
    layers = []
    M_lb = np.where(lb <= image.M, 1, 0)
    M_ub = np.where(image.M <= ub, 1, 0)
    M = np.where(M_lb + M_ub == 2, 0, 1)
    image = netpbm.Netpbm(w=w, h=h, k=1, M=M)
    return netpbm.border(image, b, c)


# COMPILE PIECES | 2021-03-23

# single prints

pieces = [('beebe_trail', 8, 0, 0, 75, "black"),
          ('road_day', 8, 0, 0, 75, "black"),
          ('creek', 8, 0, 0, 75, "black"),
          ('tree_light', 8, 1, 2, 75, "black"),
          ('buildings_night', 8, 2, 3, 75, "black"),
          ('porch', 8, 4, 8, 75, "black"),
          ('wall_light', 8, 5, 6, 75, "black"),
          ('laundry', 8, 0, 1, 75, "black")]

log = []
for name, k, lb, ub, b, c in pieces:
    file_path = "%s/%s_clip_%d_%d.pgm" % (SOURCE_DIR, name, lb, ub)
    pbm_path = '%s/%s.pbm' % (SOURCE_DIR, name)
    file_log = netpbm.transform(in_path=pbm_path, out_path=file_path, f=clip,
                                k=k, lb=lb, ub=ub, b=b, c=c, scale=1000)
    log.append(file_log)

write_log('%s/%s' % (SOURCE_DIR, 'clip.log'), log)
