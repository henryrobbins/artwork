import numpy as np
from dmtools import netpbm
from dmtools import colorspace
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
    h,w = M.shape
    image = netpbm.Netpbm(P=2, w=w, h=h, k=image.k, M=M)
    image.set_max_color_value(k)
    P = image.P
    layers = []
    for i in range(k):
        M = np.where(image.M == i,k,0)
        layers.append(netpbm.Netpbm(P=2, w=w, h=h, k=k, M=M))
    for i in range(k):
        M = np.where(image.M == i,0,k)
        layers.append(netpbm.Netpbm(P=2, w=w, h=h, k=k, M=M))
    for i in range(k):
        M = np.where(image.M == i,i,0)
        layers.append(netpbm.Netpbm(P=2, w=w, h=h, k=k, M=M))
    for i in range(k):
        M = np.where(image.M == i,0,i)
        layers.append(netpbm.Netpbm(P=2, w=w, h=h, k=k, M=M))
    return netpbm.image_grid(layers,k,4,b)


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
    file_path = "%s_partition_%d.pgm" % (name, k)
    ppm_path = '%s.ppm' % name
    netpbm.transform(in_path=ppm_path, out_path=file_path,
                     f=partition, k=k, b=b, scale=2000)
    works.append("%s_partition_%d.pgm" % (name, k))

with open("works.txt", "w") as f:
    for work in works:
        f.write("%s\n" % work)
