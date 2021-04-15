import numpy as np

import os
import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)
from netpbm import netpbm
from log import write_log


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


def resolution(image:netpbm.Netpbm) -> netpbm.Netpbm:
    """TODO

    Args:
        image (netpbm.Netpbm): TODO

    Returns:
        netpbm.Netpbm: TODO
    """
    M = image.M
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
    return netpbm.Netpbm(P=image.P, w=image.w, h=image.h, k=image.k, M=M)


# COMPILE PIECES | 2021-04-04

pieces = [('paper', 2),
          ('florida', 3)]

log = []
for name, p in pieces:
    file_path = "%s/%s_resolution.ppm" % (SOURCE_DIR, name)
    ppm_path = '%s/%s.ppm' % (SOURCE_DIR, name)
    file_log = netpbm.transform(in_path=ppm_path, out_path=file_path,
                                magic_number=p, f=resolution, scale=-1)
    log.append(file_log)


write_log('%s/%s' % (SOURCE_DIR, 'resolution.log'), log)
