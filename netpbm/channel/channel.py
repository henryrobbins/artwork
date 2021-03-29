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
    pixels = image.M.flatten() / k
    rgb = [pixels[n:n+3] for n in range(0, len(pixels), 3)]
    rgb = [[f_R(r), f_G(g), f_B(b)] for r,g,b in rgb]
    M = (np.array(rgb).reshape(n,m).clip(0,1)*k).astype(int)
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
