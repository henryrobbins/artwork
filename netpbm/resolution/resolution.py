import numpy as np
from dmtools import netpbm
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


def resolution(image:netpbm.Netpbm) -> netpbm.Netpbm:
    """TODO

    Args:
        image (netpbm.Netpbm): TODO

    Returns:
        netpbm.Netpbm: TODO
    """
    M = image.M
    if image.P == 3:
        n,m,*_ = M.shape
        M = M.reshape(n,m*3)
    else:
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
    if image.P == 3:
        M = M.reshape(n,m,3)
    return netpbm.Netpbm(P=image.P, k=image.k, M=M)


# COMPILE PIECES | 2021-04-04

pieces = [('paper', 2),
          ('florida', 3)]

works = []
for name, p in pieces:
    file_path = "%s_resolution.ppm" % name
    ppm_path = '%s.ppm' % name
    file_log = netpbm.transform(in_path=ppm_path, out_path=file_path,
                                f=resolution, scale=-1)
    works.append("%s_resolution.ppm" % name)

with open("works.txt", "w") as f:
    for work in works:
        f.write("%s\n" % work)
