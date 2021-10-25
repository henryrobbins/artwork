import numpy as np
from math import pi
from typing import Callable
import dmtools
from dmtools import colorspace
import logging
logging.basicConfig(filename='channel.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')


# Adapted from code provided by Dan Torop
def channel(image:np.ndarray, f_R:Callable,
            f_G:Callable, f_B:Callable) -> np.ndarray:
    """Return the Netpbm image after applying the functions to each channel.

    Args:
        image (np.ndarray): Image to modify.
        f_R (Callable): Function to apply to the red channel.
        f_G (Callable): Function to apply to the green channel.
        f_B (Callable): Function to apply to the blue channel.

    Returns:
        np.ndarray: NumPy matrix with modified channels.
    """
    M = image
    M = colorspace.normalize(M, 'RGB')
    M = colorspace.apply_to_channels(M, f_R, f_G, f_B)
    M = colorspace.denormalize(M, 'RGB')
    return M


# COMPILE PIECES | 2021-03-29

identity = (lambda x: x, "x")
invert = (lambda x: 1 - x, "1-x")
zero = (lambda x: 0, "0")
half = (lambda x: 0.5, "0.5")
one = (lambda x: 1, "1")


def abs_sin(p):
    return (lambda x: abs(np.sin(x*p)), "abs(sin(x*%d))" % p)


def abs_sin_sft(p):
    return (lambda x: abs(np.sin(x*p+p)), "abs(sin(x*%d+%d))" % (p,p))


def ceiling(p):
    return (lambda x: np.ceil(x*p)/p, "ceil(x*%d)_over_%d" % (p,p))


def triangle(a,p):
    return (lambda x: abs((2*a*np.arcsin(np.sin((2*pi*x)/(p))))/(pi)),
            "triangle_%0.1f_%0.1f" % (a,p))


def multiply(p):
    return (lambda x: x*p, "%0.1fx" % p)


pieces = [('math', abs_sin(5), identity, identity),
          ('math', abs_sin(10), identity, identity),
          ('math', identity, abs_sin(5), identity),
          ('math', identity, identity, abs_sin(10)),
          ('math', abs_sin(10), identity, abs_sin_sft(10)),
          ('math', ceiling(5), identity, identity),
          ('math', triangle(1.0,0.4), identity, identity),
          ('math', identity, identity, triangle(1.0,0.4)),
          ('math', invert, identity, identity),
          ('math', invert, invert, invert)]

works = []
for name, R, G, B in pieces:
    f_R, f_R_s = R
    f_G, f_G_s = G
    f_B, f_B_s = B
    image = dmtools.read_netpbm("%s.ppm" % name)
    image = channel(image, f_R, f_G, f_B)
    path = "%s_channel_%s_%s_%s.ppm" % (name, f_R_s, f_G_s, f_B_s)
    dmtools.write_netpbm(image, 255, path)
    works.append(path)

with open("works.txt", "w") as f:
    for work in works:
        f.write("%s\n" % work)
