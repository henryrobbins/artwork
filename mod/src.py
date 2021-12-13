import os
import numpy as np
import dmtools
from dmtools import colorspace
from dmtools.animation import to_mp4
import logging
logging.basicConfig(filename='mod.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')


def mod(image:np.ndarray, k:int) -> np.ndarray:
    """Return the Netpbm image mod k.

    Args:
        image (np.ndarray): Image to mod.
        k (int): Integer to mod the image by

    Returns:
        np.ndarray: NumPy matrix representing the mod image.
    """
    M_prime = colorspace.RGB_to_gray(image)
    M_prime = M_prime * 255
    M_prime = np.mod(M_prime, k)
    M_prime = M_prime / k
    return M_prime


# COMPILE PIECES | 2021-03-07

# single prints

pieces = [('road_day', 8),
          ('sky', 8),
          ('faces', 12),
          ('beebe_trail', 8),
          ('stomp', 25),
          ('water_cup', 7)]

os.makedirs('output', exist_ok=True)
for name, k in pieces:
    image = dmtools.read_netpbm('input/%s.ppm' % name)
    image = mod(image, k)
    path = "output/%s_mod_%d.pgm" % (name, k)
    dmtools.write_netpbm(image, k, path)

# animations

pieces = [('faces',1,150),
          ('water_cup',1,140)]

for name, lb, ub in pieces:
    image = dmtools.read_netpbm('input/%s.ppm' % name)
    frames = [mod(image,k) for k in range(lb,ub+1)]
    path = 'output/%s_mod_animation.mp4' % name
    to_mp4(frames=frames, path=path, fps=10, s=4)
