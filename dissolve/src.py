import os
import numpy as np
import copy
from typing import List
import dmtools
from dmtools import colorspace
import logging
logging.basicConfig(filename='dissolve.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')


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
    v_current = v
    v_hist = [list(v)]
    while len(np.where(v_current != 0)[0]) > 0:
        v_current = dissolve_iter(v_current)
        v_hist.append(list(v_current))
    return np.array(v_hist)


def dissolve(image:np.ndarray, modifications:List) -> np.ndarray:
    """Dissolve the Netpbm image.

    Args:
        image (np.ndarray): Image to dissolve.
        modifications (List): List of modifications ({'h','v'}, int) to apply.

    Returns:
        np.ndarray: NumPy matrix representing the dissolved image.
    """
    new_image = copy.copy(image)
    M = colorspace.RGB_to_gray(new_image)
    M = np.mod((M * 8).astype(int), 8)
    for direction, i in modifications:
        if direction == 'h':
            M = np.vstack((M[:i], dissolve_vector(M[i])))
        elif direction == 'v':
            M = np.hstack((M[:,:i], dissolve_vector(M[:,i]).T))
    M = M / 8
    return M

# COMPILE PIECES | 2021-03-02

pieces = [[('h',70)],
          [('h',100)],
          [('h',140)],
          [('v',80)],
          [('h',60),('v',47)],
          [('h',71),('v',251)]]

base_image = dmtools.read_netpbm('input/beebe_trail.ppm')

os.makedirs('output', exist_ok=True)
for piece in pieces:
    image = dissolve(base_image, piece)
    modification = ''.join([op[0] + str(op[1]) for op in piece])
    path = 'output/beebe_trail_%s.pgm' % modification
    dmtools.write_netpbm(image, 8, path)
