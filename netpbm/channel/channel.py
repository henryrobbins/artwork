import os
import time
import numpy as np
from math import ceil, pi

from typing import Callable

import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)
from netpbm import netpbm
from netpbm import colorspace
from log import write_log, collapse_log


# Adapted from code provided by Dan Torop
def channel(image:netpbm.Netpbm, f_R:Callable,
            f_G:Callable, f_B:Callable ) -> netpbm.Netpbm:
    """Return the Netpbm image after applying the functions to each channel.

    Args:
        image (netpbm.Netpbm): Netpbm image to modify.
        f_R (Callable): Function to apply to the red channel.
        f_G (Callable): Function to apply to the green channel.
        f_B (Callable): Function to apply to the blue channel.

    Returns:
        netpbm.Netpbm: NumPy matrix with modified channels.
    """
    n,m = image.M.shape
    k = image.k
    M = image.M

    # M = colorspace.normalize(M, 'RGB', True)
    # M = colorspace.apply_to_channels(M, f_R, f_G, f_B)
    # M = colorspace.normalize(M, 'RGB', False)

    # M = colorspace.RGB_to_Lab(M)
    # M = colorspace.normalize(M, 'Lab', True)
    # M = colorspace.apply_to_channels(M, f_R, f_G, f_B)
    # M = colorspace.normalize(M, 'Lab', False)
    # M = colorspace.Lab_to_RGB(M)

    M = colorspace.RGB_to_YUV(M)
    M = colorspace.normalize(M, 'YUV', True)
    M = colorspace.apply_to_channels(M, f_R, f_G, f_B)
    M = colorspace.normalize(M, 'YUV', False)
    M = colorspace.YUV_to_RGB(M)

    return netpbm.Netpbm(P=image.P, w=image.w, h=image.h, k=k, M=M)


# COMPILE PIECES | 2021-03-29

# functions
identity = (lambda x : x, "x")
abs_sin = lambda p : (lambda x : abs(np.sin(x*p)), "abs(sin(x*%d))" % p)
abs_sin_sft = lambda p : (lambda x : abs(np.sin(x*p+p)),
                          "abs(sin(x*%d+%d))" % (p,p))
ceiling = lambda p : (lambda x : ceil(x*p)/p, "frac{ceil(x*%d)}{%d}" % (p,p))
triangle = lambda a, p : (
                lambda x : abs((2*a*np.arcsin(np.sin((2*pi*x)/(p))))/(pi)),
                 "triangle_%0.1f_%0.1f" % (a,p))
invert = (lambda x : 1 - x, "1-x")
multiply = lambda p : (lambda x : x*p, "%0.1fx" % (p))
zero = (lambda x : 0, "0")
half = (lambda x : 0.5, "0.5")
one = (lambda x : 1, "1")

# 2021-03-29 -- Normal RGB edits
# pieces = [('math', abs_sin(5), identity, identity),
#           ('math', abs_sin(10), identity, identity),
#           ('math', identity, abs_sin(5), identity),
#           ('math', identity, identity, abs_sin(10)),
#           ('math', abs_sin(10), identity, abs_sin_sft(10)),
#           ('math', ceiling(5), identity, identity),
#           ('math', triangle(1.0,0.4), identity, identity),
#           ('math', identity, identity, triangle(1.0,0.4)),
#           ('math', invert, identity, identity),
#           ('math', invert, invert, invert)]

# 2021-03-31 -- Lab edits
pieces = [('math', identity, half, half),
          ('math', zero, identity, half),
          ('math', zero, half, identity),
          ('barn', identity, half, half),
          ('barn', zero, identity, half),
          ('barn', zero, half, identity),
          ('math', multiply(1.3), identity, identity),
          ('math', identity, multiply(1.3), identity),
          ('math', identity, identity, multiply(1.3)),
          ('barn', multiply(1.3), identity, identity),
          ('barn', identity, multiply(1.3), identity),
          ('barn', identity, identity, multiply(1.3))]

log = []
for name, R, G, B in pieces:
    f_R, f_R_s = R
    f_G, f_G_s = G
    f_B, f_B_s = B
    file_path = "%s/%s_channel_%s_%s_%s.ppm" % (SOURCE_DIR, name,
                                                f_R_s, f_G_s, f_B_s)
    ppm_path = '%s/%s.ppm' % (SOURCE_DIR, name)
    file_log = netpbm.transform(in_path=ppm_path, out_path=file_path,
                                f=channel, f_R=f_R, f_B=f_B, f_G=f_G)
    log.append(file_log)

write_log('%s/%s' % (SOURCE_DIR, 'channel.log'), log)
