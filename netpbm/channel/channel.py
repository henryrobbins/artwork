import os
import time
import numpy as np
from math import ceil
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

pieces = [('math', lambda x : x*2,  "x*2",
                   lambda x : x,    "x",
                   lambda x : x,    "x"),
          ('math', lambda x : x,    "x",
                   lambda x : x*2,  "x*2",
                   lambda x : x,    "x"),
          ('math', lambda x : x,    "x",
                   lambda x : x,    "x",
                   lambda x : x*2,  "x*2"),
          ('math', lambda x : abs(np.sin(x*5)), "abs(sin(x*5))",
                   lambda x : x,                "x",
                   lambda x : x,                "x")]

log = []
for name, f_R, f_R_s, f_G, f_G_s, f_B, f_B_s in pieces:
    file_path = "%s/%s_channel_%s_%s_%s.ppm" % (SOURCE_DIR, name,
                                                f_R_s, f_G_s, f_B_s)
    ppm_path = '%s/%s.ppm' % (SOURCE_DIR, name)
    file_log = netpbm.transform(in_path=ppm_path, out_path=file_path,
                                f=channel, f_R=f_R, f_B=f_B, f_G=f_G,
                                scale=1000)
    log.append(file_log)

write_log('%s/%s' % (SOURCE_DIR, 'mod.log'), log)
