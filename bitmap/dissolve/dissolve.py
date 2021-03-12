import numpy as np
import os
from typing import List

import sys
sys.path.insert(1, '../')
import netpbm
sys.path.insert(1, '../../')
from log import write_log


def dissolve_iter(v:np.ndarray) -> np.ndarray:
    """Return vector v after one iteration of dissolving."""
    n = len(v)
    v_new = []
    for i in range(n):
        l = 0 if i-1 < 0 else v[i-1]
        r = 0 if i+1 >= n else v[i+1]
        x = v[i]
        if x != 0:
            if (x > l) & (x > r):
                x_new = x - 2
            elif (x < l) & (x < r):
                x_new = x + 2
            elif ((x == l) & (x < r)) | ((x == r) & (x < l)):
                x_new = x + 1
            elif ((x == l) & (x > r)) | ((x == r) & (x > l)):
                x_new = x - 1
            else:
                x_new = x
        else:
            x_new = x
        v_new.append(max(0,x_new))
    return np.array(v_new)


def dissolve_vector(v:np.ndarray) -> np.ndarray:
    """Return the evolution of v as it dissolves completely."""
    n = len(v)
    v_current = v
    v_hist = [list(v)]
    while len(np.where(v_current != 0 )[0]) > 0:
        v_current = dissolve_iter(v_current)
        v_hist.append(list(v_current))
    return np.array(v_hist)


def dissolve(image:netpbm.Netpbm, modifications:List) -> netpbm.Netpbm:
    """Dissolve the Netpbm image.

    Args:
        image (netpbm.Netpbm): Netpbm image to dissolve.
        modifications (List): List of modifications ({'h','v'}, int) to apply.

    Returns:
        netpbm.Netpbm: NumPy matrix representing the dissolved image.
    """
    image = netpbm.change_gradient(image, 8)
    for direction, i in modifications:
        if direction == 'h':
            M = np.vstack((image.M[:i], dissolve_vector(image.M[i])))
        elif direction == 'v':
            M = np.hstack((image.M[:,:i], dissolve_vector(image.M[:,i]).T))
        h,w = M.shape
        image = netpbm.Netpbm(w=w, h=h, k=image.k, M=M)
    return image


# COMPILE PIECES | 2021-03-02

pieces = [[('h',70)],
          [('h',100)],
          [('h',140)],
          [('v',80)],
          [('h',60),('v',47)],
          [('h',71),('v',251)]]

log = []
for piece in pieces:
    modification = ''.join([op[0] + str(op[1]) for op in piece])
    file_name = 'beebe_trail_%s.pgm' % modification
    file_log = netpbm.compile(path='./%s' % file_name,
                              pbm_path='beebe_trail.pbm',
                              f=dissolve,
                              scale=1000,
                              modifications=piece)
    log.append(file_log)

write_log('dissolve.log', log)
