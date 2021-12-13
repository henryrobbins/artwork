import os
import numpy as np
from scipy.signal import convolve2d
import dmtools
from dmtools import colorspace
from dmtools.animation import to_mp4

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

os.makedirs('output', exist_ok=True)
for name, g in pieces:
    path = 'input/%s.ppm' % (name)

    image = dmtools.read_netpbm(path)
    base_M = colorspace.RGB_to_gray(image)
    M = colorspace.RGB_to_gray(image)
    M = np.where(M > 0.5, 1, 0)

    frames = [conway(M)]
    for i in range(g):
        frames.append(conway(frames[-1]))
    base_M = base_M * np.where(frames[0] == 1,0,1)
    frames = [base_M * np.where(f == 1,0,1) for f in frames]

    file_name = 'output/%s_conway_animation.mp4' % name
    to_mp4(frames=frames, path=file_name, fps=45, s=8)

    frames = frames[::-1]
    file_name = 'output/%s_reverse_conway_animation.mp4' % name
    to_mp4(frames=frames, path=file_name, fps=45, s=8)
