import numpy as np
from dmtools import netpbm, colorspace, arrange
import logging
logging.basicConfig(filename='partition.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')


def partition(image:netpbm.Netpbm, k:int, b:int) -> netpbm.Netpbm:
    """Return the Netpbm image mod k.

    Args:
        image (netpbm.Netpbm): Netpbm image to mod.
        k (int): Number of gradients.
        b (int): Width of the border in pixels.

    Returns:
        netpbm.Netpbm: NumPy matrix representing the mod image.
    """
    M = colorspace.RGB_to_gray(image.M)
    image = netpbm.Netpbm(P=2, k=image.k, M=M)
    image.set_max_color_value(k)
    P = image.P
    layers = []
    for i in range(k):
        layers.append(np.where(image.M == i,k,0))
    for i in range(k):
        layers.append(np.where(image.M == i,0,k))
    for i in range(k):
        layers.append(np.where(image.M == i,i,0))
    for i in range(k):
        layers.append(np.where(image.M == i,0,i))

    image_grid = arrange.image_grid(layers,k,4,b,k=k)
    return netpbm.Netpbm(P=2, k=k, M=image_grid)


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
works = []
for name, k, b in pieces:
    image = netpbm.read_netpbm('%s.ppm' % name)
    image = partition(image, k, b)
    path = "%s_partition_%d.pgm" % (name, k)
    image.to_netpbm(path)
    works.append(path)

with open("works.txt", "w") as f:
    for work in works:
        f.write("%s\n" % work)
