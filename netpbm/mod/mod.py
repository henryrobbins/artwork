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
    return netpbm.Netpbm(w=w, h=h, k=k, M=M_prime)


# COMPILE PIECES | 2021-03-07

# single prints

pieces = [('road_day', 8),
          ('sky', 8),
          ('faces', 12),
          ('beebe_trail', 8),
          ('stomp', 25),
          ('water_cup', 7)]

log = []
for name, k in pieces:
    file_path = "%s/%s_mod_%d.pgm" % (SOURCE_DIR, name, k)
    pbm_path = '%s/%s.pbm' % (SOURCE_DIR, name)
    file_log = netpbm.compile(path=file_path, pbm_path=pbm_path,
                              f=mod, k=k, scale=1000)
    log.append(file_log)

# animations

pieces = [('faces',1,150)]

for name, lb, ub in pieces:
    tmp_logs = []
    if not os.path.isdir("%s/%s" % (SOURCE_DIR, name)):
        os.mkdir("%s/%s" % (SOURCE_DIR, name))
    for k in range(lb,ub+1):
        file_path = "%s/%s/%s_mod_%s.pgm" % (SOURCE_DIR, name, name, str(k).zfill(3))
        pbm_path = '%s/%s.pbm' % (SOURCE_DIR, name)
        file_log = netpbm.compile(path=file_path, pbm_path=pbm_path,
                                  f=mod, k=k)
        tmp_logs.append(file_log)
    log.append(collapse_log(name, tmp_logs))

write_log('%s/%s' % (SOURCE_DIR, 'mod.log'), log)