import os
import numpy as np
import dmtools
from dmtools import colorspace, arrange
import logging
logging.basicConfig(filename='partition.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')


def partition(image:np.ndarray, k:int, b:int) -> np.ndarray:
    """Return the Netpbm image mod k.

    Args:
        image (np.ndarray): Image to mod.
        k (int): Number of gradients.
        b (int): Width of the border in pixels.

    Returns:
       np.ndarray: NumPy matrix representing the mod image.
    """
    M = colorspace.RGB_to_gray(image)
    image = np.mod((M * k).astype(int), k)

    layers = []
    for i in range(k):
        layers.append(np.where(image == i,k,0))
    for i in range(k):
        layers.append(np.where(image == i,0,k))
    for i in range(k):
        layers.append(np.where(image == i,i,0))
    for i in range(k):
        layers.append(np.where(image == i,0,i))

    layers = [layer / k for layer in layers]
    image_grid = arrange.image_grid(layers,k,4,b)
    return image_grid


# COMPILE PIECES | 2021-03-20

# single prints

pieces = [('road_day', 8, 30),
          ('sky', 8, 30),
          ('tree', 8, 30),
          ('beebe_day', 8, 30),
          ('waterfall', 8, 30),
          ('risley', 8, 30),
          ('creek', 8, 30),
          ('fallen_tree', 8, 30),
          ('old_man', 8, 30),
          ('wading', 8, 30),
          ('island', 8, 30)]

os.makedirs('output', exist_ok=True)
for name, k, b in pieces:
    image = dmtools.read_netpbm('input/%s.ppm' % name)
    image = partition(image, k, b)
    path = "output/%s_partition_%d.pgm" % (name, k)
    dmtools.write_netpbm(image, k, path)
