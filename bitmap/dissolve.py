import netpbm
import numpy as np
import os
import time
from math import ceil
from typing import List

import sys
sys.path.insert(1, '../')
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


def dissolve_image(M:np.ndarray, direction:str, i:int) -> np.ndarray:
    """Dissolve the image.

    Args:
        np.ndarray: NumPy matrix representing the Netpbm file.
        direction (str): Direction to dissolve the image in {'h','v'}.
        int (i): Row / column index to dissolve the image from.

    Returns:
        np.ndarray: NumPy matrix representing the dissolved image.
    """
    if direction == 'h':
        M_prime = np.vstack((M[:i], dissolve_vector(M[i])))
    elif direction == 'v':
        M_prime = np.hstack((M[:,:i], dissolve_vector(M[:,i]).T))
    return M_prime


# COMPILE PIECES | 2021-03-02

netpbm.convert_from_p6('dissolve/beebe_trail.pbm')
M, w, h, n = netpbm.read('dissolve/beebe_trail.pgm')
M = netpbm.change_gradient(M, n, 8)

pieces = [[('h',70)],
          [('h',100)],
          [('h',140)],
          [('v',80)],
          [('h',60),('v',47)],
          [('h',71),('v',251)]]

log = []  # keep track of compilation time and file sizes
for piece in pieces:
    then = time.time()
    name = ''.join([op[0] + str(op[1]) for op in piece])
    M_prime = M
    for direction, i in piece:
        M_prime = dissolve_image(M_prime, direction, i)
    k  = ceil(1000 / max(M_prime.shape))
    M_prime = netpbm.enlarge(M_prime, k)
    file_name = 'beebe_trail_%s.pgm' % (name)
    netpbm.write('dissolve/%s' % (file_name), M_prime, 8)

    t = time.time() - then
    size = os.stat('dissolve/%s' % (file_name)).st_size
    log.append({'name':file_name, 't':'%.3f' % t, 'size':'%d' % size})

write_log('dissolve/dissolve.log', log)
