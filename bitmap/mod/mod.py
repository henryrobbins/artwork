import os
import time
import numpy as np
from math import ceil

import sys
sys.path.insert(1, '../')
import netpbm
sys.path.insert(1, '../../')
from log import write_log


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
          ('sky', 8),           # photo taken by Ella Clemons (2/24/2021)
          ('faces', 12),        # photo taken by Ella Clemons (3/7/2021)
          ('beebe_trail', 8),
          ('stomp', 25),        # photo taken by Ella Clemons (3/7/2021)
          ('water_cup', 7)]     # photo taken by Ella Clemons (3/7/2021)

log = []  # keep track of compilation time and file sizes
for name, k in pieces:
    file_name = "%s_mod_%d.pgm" % (name, k)
    file_log = netpbm.compile(path=file_name,
                              pbm_path='%s.pbm' % name,
                              f=mod, k=k,
                              scale=1000)
    log.append(file_log)

# animations

pieces = [('faces',1,150)]      # photo taken by Ella Clemons (3/7/2021)

for name, lb, ub in pieces:
    if not os.path.isdir(name):
        os.mkdir(name)
    for k in range(lb,ub+1):
        file_name = "%s_mod_%s.pgm" % (name, str(k).zfill(3))
        file_log = netpbm.compile(path='%s/%s' % (name, file_name),
                                  pbm_path='%s.pbm' % name,
                                  f=mod, k=k)
        log.append(file_log)

write_log('mod.log', log)
