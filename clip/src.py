import os
import numpy as np
import dmtools
from dmtools import colorspace, arrange
from assistant.help import get_metadata

def clip(image:np.ndarray,
         k:int, lb:int, ub:int, b:int, c:str) -> np.ndarray:
    """Return the Netpbm image mod k.

    Args:
        image (np.ndarray): Image to mod.
        k (int): Number of gradients.
        lb (int): Lower bound of gradients to show.
        ub (int): Upper bound of gradients to show.
        b (int): Width of the border.
        c (str): Color of the border {'white', 'black'}

    Returns:
        np.ndarray: NumPy matrix representing the mod image.
    """
    M = colorspace.RGB_to_gray(image)
    image = np.mod((M * k).astype(int), k)
    M_lb = np.where(lb <= image, 1, 0)
    M_ub = np.where(image <= ub, 1, 0)
    M = np.where(M_lb + M_ub == 2, 0, 1)
    bordered_image = arrange.border(M, b, c)
    return bordered_image


# COMPILE PIECES | 2021-03-23

# single prints

pieces = [('beebe_trail', 8, 0, 0, 75, 0),
          ('road_day', 8, 0, 0, 75, 0),
          ('creek', 8, 0, 0, 75, 0),
          ('tree_light', 8, 1, 2, 75, 0),
          ('buildings_night', 8, 2, 3, 75, 0),
          ('porch', 8, 4, 8, 75, 0),
          ('wall_light', 8, 5, 6, 75, 0),
          ('laundry', 8, 0, 1, 75, 0)]

os.makedirs('output', exist_ok=True)
for name, k, lb, ub, b, c in pieces:
    image = dmtools.read_netpbm('input/%s.ppm' % name)
    image = clip(image, k=k, lb=lb, ub=ub, b=b, c=c)
    path = "output/%s_clip_%d_%d.pgm" % (name, lb, ub)
    dmtools.write_netpbm(image, k, path, metadata=get_metadata())
