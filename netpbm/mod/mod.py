import os
import numpy as np
from dmtools import netpbm
from dmtools.animation import animation
import logging
logging.basicConfig(filename='mod.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))

def mod(image:netpbm.Netpbm, k:int) -> netpbm.Netpbm:
    """Return the Netpbm image mod k.

    Args:
        image (netpbm.Netpbm): Netpbm image to mod.
        k (int): Integer to mod the image by

    Returns:
        netpbm.Netpbm: NumPy matrix representing the mod image.
    """
    M_prime = np.array(list(map(lambda x: x % k, image.M)))
    h,w = M_prime.shape
    return netpbm.Netpbm(P=image.P, w=w, h=h, k=k, M=M_prime)


# COMPILE PIECES | 2021-03-07

# single prints

pieces = [('road_day', 8),
          ('sky', 8),
          ('faces', 12),
          ('beebe_trail', 8),
          ('stomp', 25),
          ('water_cup', 7)]

works = []
for name, k in pieces:
    file_path = "%s/%s_mod_%d.pgm" % (SOURCE_DIR, name, k)
    ppm_path = '%s/%s.ppm' % (SOURCE_DIR, name)
    netpbm.transform(in_path=ppm_path, out_path=file_path,
                     magic_number=2, f=mod, k=k, scale=1000)
    works.append("%s_mod_%d.pgm" % (name, k))

# animations

pieces = [('faces',1,150),
          ('water_cup',1,140)]

for name, lb, ub in pieces:
    path = '%s/%s.ppm' % (SOURCE_DIR, name)
    M = netpbm.read(netpbm.raw_to_plain(path, magic_number=2))
    frames = [mod(M,k).M * (255/k) for k in range(lb,ub+1)]
    file_name = '%s/%s_mod_animation.mp4' % (SOURCE_DIR, name)
    animation(frames=frames, path=file_name, fps=10, s=4)
    works.append("%s_mod_animation.mp4" % name)

with open("works.txt", "w") as f:
    for work in works:
        f.write("%s\n" % work)
