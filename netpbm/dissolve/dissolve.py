import numpy as np
import copy
from typing import List
from dmtools import netpbm
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


def dissolve(image:netpbm.Netpbm, modifications:List) -> netpbm.Netpbm:
    """Dissolve the Netpbm image.

    Args:
        image (netpbm.Netpbm): Netpbm image to dissolve.
        modifications (List): List of modifications ({'h','v'}, int) to apply.

    Returns:
        netpbm.Netpbm: NumPy matrix representing the dissolved image.
    """
    new_image = copy.copy(image)
    new_image.set_max_color_value(8)
    M = colorspace.RGB_to_gray(new_image.M)
    for direction, i in modifications:
        if direction == 'h':
            M = np.vstack((M[:i], dissolve_vector(M[i])))
        elif direction == 'v':
            M = np.hstack((M[:,:i], dissolve_vector(M[:,i]).T))
    return netpbm.Netpbm(P=2, k=8, M=M)


# COMPILE PIECES | 2021-03-02

pieces = [[('h',70)],
          [('h',100)],
          [('h',140)],
          [('v',80)],
          [('h',60),('v',47)],
          [('h',71),('v',251)]]

base_image = netpbm.read_netpbm('beebe_trail.ppm')

works = ["dissolve.pgm", "dissolve2.pgm", "dissolve3.pgm"]
for piece in pieces:
    image = dissolve(base_image, piece)
    modification = ''.join([op[0] + str(op[1]) for op in piece])
    path = 'beebe_trail_%s.pgm' % modification
    image.to_netpbm(path)
    works.append(path)

with open("works.txt", "w") as f:
    for work in works:
        f.write("%s\n" % work)
