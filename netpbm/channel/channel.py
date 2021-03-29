import os
import time
import numpy as np
from math import ceil

import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)
from netpbm import netpbm
from log import write_log, collapse_log


def channel(image:netpbm.Netpbm) -> netpbm.Netpbm:
    """TODO

    Args:
        image (netpbm.Netpbm): Netpbm image to TODO

    Returns:
        netpbm.Netpbm: NumPy matrix representing TODO
    """
    # TODO
    #  return netpbm.Netpbm(P=image.P, w=w, h=h, k=k, M=M_prime)
    return image


# COMPILE PIECES | 2021-03-29

pieces = [('math')]

log = []
for name in pieces:
    file_path = "%s/%s_channel.ppm" % (SOURCE_DIR, name)
    ppm_path = '%s/%s.ppm' % (SOURCE_DIR, name)
    file_log = netpbm.transform(in_path=ppm_path, out_path=file_path,
                                f=channel, scale=1000)
    log.append(file_log)

write_log('%s/%s' % (SOURCE_DIR, 'mod.log'), log)
