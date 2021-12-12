import os
import numpy as np
import dmtools
from dmtools import colorspace
import logging
logging.basicConfig(filename='resolution.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')


def shrink(M:np.ndarray, d:int) -> np.ndarray:
    """Return the matrix M at the resolution d x d.

    Args:
        M (np.ndarray): Numpy matrix with dimensions multiples of d.
        d (int): Resolution of the resulting matrix.

    Returns:
        np.ndarray: Original matrix at resolution d.
    """
    n,m = M.shape
    assert n % d == 0
    assert m % d == 0
    for i in range(d):
        for j in range(d):
            s = int(n/d)
            A = M[s*i:s*(i+1), s*j:s*(j+1)]
            v = np.mean(A)
            B = np.ones((s,s))*v
            M[s*i:s*(i+1), s*j:s*(j+1)] = B
    return M


def resolution(image:np.ndarray) -> np.ndarray:
    """Return image with resolution based on brightness.

    Args:
        image (np.ndarray): Image to alter.

    Returns:
        np.ndarray: NumPy matrix representing the altered image.
    """
    M = image
    M = colorspace.RGB_to_gray(M)
    M = M * 255
    n,m = M.shape
    assert n % 256 == 0
    assert m % 256 == 0
    for i in range(int(n/256)):
        for j in range(int(m/256)):
            A = M[256*i:256*(i+1), 256*j:256*(j+1)]
            v = np.mean(A)
            if v >= 150:
                B = shrink(A,4)
            elif v >= 128:
                B = shrink(A,8)
            else:
                B = shrink(A, 32)
            M[256*i:256*(i+1), 256*j:256*(j+1)] = B
    M = M / 255
    return M


# COMPILE PIECES | 2021-04-04

pieces = [('paper', 2),
          ('florida', 3)]

os.makedirs('output', exist_ok=True)
for name, p in pieces:
    image = dmtools.read_netpbm('input/%s.ppm' % name)
    image = resolution(image)
    path = "output/%s_resolution.pgm" % name
    dmtools.write_netpbm(image, 255, path)
