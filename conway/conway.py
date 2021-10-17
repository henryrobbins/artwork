import numpy as np
from scipy.signal import convolve2d
from dmtools import netpbm, colorspace
from dmtools.animation import to_mp4
import logging
logging.basicConfig(filename='conway.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')

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
    path = '%s.ppm' % (name)

    image = netpbm.read_netpbm(path)
    base_M = colorspace.RGB_to_gray(image.M)
    M = colorspace.RGB_to_gray(image.M)
    image = netpbm.Netpbm(P=2, k=image.k, M=M)
    image.set_max_color_value(1)
    M = image.M

    frames = [conway(M)]
    for i in range(g):
        frames.append(conway(frames[-1]))
    base_M = base_M * np.where(frames[0] == 1,0,1)
    frames = [base_M * np.where(f == 1,0,1) for f in frames]

    file_name = '%s_conway_animation.mp4' % name
    to_mp4(frames=frames, path=file_name, fps=45, s=8)
    works.append("%s_conway_animation.mp4" % name)

    frames = frames[::-1]
    file_name = '%s_reverse_conway_animation.mp4' % name
    to_mp4(frames=frames, path=file_name, fps=45, s=8)
    works.append("%s_reverse_conway_animation.mp4" % name)

with open("works.txt", "w") as f:
    for work in works:
        f.write("%s\n" % work)
