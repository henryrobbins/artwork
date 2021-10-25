import numpy as np
import dmtools
from dmtools import colorspace, arrange
import logging
logging.basicConfig(filename='clip.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')

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

pieces = [('beebe_trail', 8, 0, 0, 75, "black"),
          ('road_day', 8, 0, 0, 75, "black"),
          ('creek', 8, 0, 0, 75, "black"),
          ('tree_light', 8, 1, 2, 75, "black"),
          ('buildings_night', 8, 2, 3, 75, "black"),
          ('porch', 8, 4, 8, 75, "black"),
          ('wall_light', 8, 5, 6, 75, "black"),
          ('laundry', 8, 0, 1, 75, "black")]

works = []
for name, k, lb, ub, b, c in pieces:
    image = dmtools.read_netpbm('%s.ppm' % name)
    image = clip(image, k=k, lb=lb, ub=ub, b=b, c=c)
    path = "%s_clip_%d_%d.pgm" % (name, lb, ub)
    dmtools.write_netpbm(image, k, path)
    works.append(path)

with open("works.txt", "w") as f:
    for work in works:
        f.write("%s\n" % work)
