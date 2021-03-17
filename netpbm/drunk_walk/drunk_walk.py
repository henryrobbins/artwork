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


def rand_move(x:int, y:int, M:np.ndarray):
    """Move from x,y to an adjacent location randomly. Add one to the elemenet
    that is visited next.

    Args:
        x (int): x-coordinate of current location.
        y (int): y-coordinate of current location.
        M (np.ndarray): board on which to move.
    """
    n,m = M.shape
    move = random.randint(0,3)
    if move == 0: x += 1
    if move == 1: x -= 1
    if move == 2: y += 1
    if move == 3: y -= 1
    M[x % n][y % m] += 1
    return x,y,M


def drunk_walk(n:int, x:int, y:int, M:np.ndarray):
    """Do an n-step drunk walk from (x,y) on M.

    Args:
        n (int): number of steps to take.
        x (int): x-coordinate of start location.
        y (int): y-coordinate of start location.
        M (np.ndarray): board on which to walk.
    """
    for i in range(n):
        x,y,M = rand_move(x,y,M)
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
    M = np.array(list(map(lambda x: x % k, M)))
    return netpbm.Netpbm(d,d,k,M.astype(int))


def drunk_walk_series(n:int, k:int, d:int, w:int, h:int, b:int):
    """Create a w*h grid d*d drunk walk with n steps on k gradients.

    Args:
        n (int): number of steps to take.
        k (int): number of gradients.
        d (int): dimension of the board on which to walk.
        w (int): number of boards in each row of the grid.
        h (int): number of boards in each column of the grid.
        b (int): width of the border/margin.
    """
    h_border = k*np.ones((b, w*d + (w+1)*b))
    v_border = k*np.ones((d, b))
    image = h_border
    for i in range(h):
        row = v_border
        for j in range(w):
            M = drunk_walk_image(n,k,d).M
            row = np.hstack((row, M))
            row = np.hstack((row, v_border))
        image = np.vstack((image, row))
        image = np.vstack((image, h_border))
    return netpbm.Netpbm(w=w*d + (w+1)*b,
                         h=h*d + (h+1)*b,
                         k=k, M=image.astype(int))


# COMPILE PIECES | 2021-03-17

pieces = [(4096, 4, 128, 3, 3, 8),
          (4, 4, 2, 3, 3, 1),
          (1024, 4, 32, 3, 3, 4),
          (256, 4, 16, 3, 3, 2),
          (64, 4, 8, 3, 3, 2),
          (16, 4, 4, 3, 3, 1)]

log = []
for n, k, d, w, h, b in pieces:
    then = time.time()

    image = drunk_walk_series(n, k, d, w, h, b)
    m = ceil(1000 / max(image.M.shape))
    image = netpbm.enlarge(image, m)

    name = '%d' % n
    path = '%s/%s_step_drunk_walk.pgm' % (SOURCE_DIR, name)
    netpbm.write(path, image)

    t = time.time() - then
    size = os.stat(path).st_size
    name = path.split('/')[-1]
    log.append(Log(name=name, time=t, size=size))

write_log('%s/%s' % (SOURCE_DIR, 'drunk_walk.log'), log)
