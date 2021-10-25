import numpy as np
import dmtools
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
    """TODO

    Args:
        image (np.ndarray): TODO

    Returns:
        np.ndarray: TODO
    """
    M = image
    if len(image.shape) == 3:
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
    if len(image.shape) == 3:
        M = M.reshape(n,m,3)
    return M


# COMPILE PIECES | 2021-04-04

pieces = [('paper', 2),
          ('florida', 3)]

works = []
for name, p in pieces:
    image, k = dmtools.read_netpbm('%s.ppm' % name)
    image = resolution(image)
    path = "%s_resolution.ppm" % name
    dmtools.write_netpbm(image, k, path)
    works.append(path)

with open("works.txt", "w") as f:
    for work in works:
        f.write("%s\n" % work)
