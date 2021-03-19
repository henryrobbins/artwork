import time
import numpy as np
from math import ceil
import random
random.seed(3699)

import os, sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)
from netpbm import netpbm
from log import Log, write_log, collapse_log


def drunk_walk(k:int, x:int, y:int, M:np.ndarray):
    """Do a k-step drunk walk from (x,y) on M.

    Args:
        k (int): number of steps to take.
        x (int): x-coordinate of start location.
        y (int): y-coordinate of start location.
        M (np.ndarray): board on which to walk.
    """
    n,m = M.shape
    for i in range(k):
        move = random.randint(0,3)
        if move == 0: x += 1
        if move == 1: x -= 1
        if move == 2: y += 1
        if move == 3: y -= 1
        M[x % n][y % m] += 1
    return M


def drunk_walk_image(n:int, k:int, d:int):
    """Create a d*d drunk walk with n steps on k gradients.

    Args:
        n (int): number of steps to take.
        k (int): number of gradients.
        d (int): dimension of the board on which to walk.
    """
    c = int(d/2)
    M = np.zeros((d,d))
    x = random.randint(0,d)
    y = random.randint(0,d)
    M = drunk_walk(n,x,y,M)
    # This implementation makes more sense but not as interesting..
    # M = np.clip(M, 0, k)
    M = np.array(list(map(lambda x: x % k, M)))
    return netpbm.Netpbm(d,d,k,M.astype(int))


def drunk_walk_series(n:int, k:int, d:int, w:int, h:int, b:int) -> netpbm.Netpbm:
    """Create a series of d*d drunk walk with n steps on k gradients.

    Args:
        n (int): number of steps to take.
        k (int): number of gradients.
        d (int): dimension of the board on which to walk.
        w (int): number of boards per row of the grid.
        h (int): number of boards per column of the grid.
        b (int): width of the border/margin.

    Returns:
        netpbm.Netpbm: Image of the series of drunk walks.
    """
    images = [drunk_walk_image(n,k,d) for i in range(w*h)]
    return netpbm.image_grid(images,w,h,b)


# COMPILE PIECES | 2021-03-17

pieces = [(4096, 4, 128, 3, 3, 8),
          (4, 4, 2, 3, 3, 1),
          (1024, 4, 32, 3, 3, 4),
          (256, 4, 16, 3, 3, 2),
          (64, 4, 8, 3, 3, 2),
          (16, 4, 4, 3, 3, 1)]

log = []
for n, k, d, w, h, b in pieces:
    name = '%d' % n
    path = '%s/%s_step_drunk_walk.pgm' % (SOURCE_DIR, name)
    log.append(netpbm.generate(path=path, f=drunk_walk_series, scale=1000,
                               n=n, k=k, d=d, w=w, h=h, b=b))

write_log('%s/%s' % (SOURCE_DIR, 'drunk_walk.log'), log)
