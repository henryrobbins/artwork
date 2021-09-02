import numpy as np
from scipy.signal import convolve2d
import os
from dmtools import netpbm
from dmtools.animation import animation
import logging
logging.basicConfig(filename='conway.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))

# This code was provided by Dan Torop for ART 3699
COUNT_NEIGHBORS = np.array([[1,1,1],
                            [1,0,1],
                            [1,1,1]])


def conway(M:np.ndarray) -> np.ndarray:
    """Return image after one iteration of Conway's Game of Life.

    Args:
        image (np.ndarray): Current world state of Conway's Game of Life.

    Returns:
        np.ndarray: Current world state one iteration in the future.
    """
    # This code was provided by Dan Torop for ART 3699
    neighbors = convolve2d(M, COUNT_NEIGHBORS, mode="same", boundary="wrap")
    survive = M & ((neighbors == 2) | (neighbors == 3))
    born = neighbors == 3
    return survive | born


# COMPILE PIECES | 2021-05-02

pieces = [('node', 4700),
          ('rhizomes', 4750)]

works = []
for name, g in pieces:
    path = '%s/%s.ppm' % (SOURCE_DIR, name)

    base_M = netpbm.read(netpbm.raw_to_plain(path, magic_number=2)).M
    M = netpbm.read(netpbm.raw_to_plain(path, magic_number=1)).M

    frames = [conway(M)]
    for i in range(g):
        frames.append(conway(frames[-1]))
    base_M = base_M * np.where(frames[0] == 1,0,1)
    frames = [base_M * np.where(f == 1,0,1) for f in frames]

    file_name = '%s/%s_conway_animation.mp4' % (SOURCE_DIR, name)
    animation(frames=frames, path=file_name, fps=45, s=8)
    works.append("%s_conway_animation.mp4" % name)

    frames = frames[::-1]
    file_name = '%s/%s_reverse_conway_animation.mp4' % (SOURCE_DIR, name)
    animation(frames=frames, path=file_name, fps=45, s=8)
    works.append("%s_reverse_conway_animation.mp4" % name)

with open("works.txt", "w") as f:
    for work in works:
        f.write("%s\n" % work)
