import os
import time
import numpy as np
from math import ceil

import sys
sys.path.insert(1, '../')
import netpbm
sys.path.insert(1, '../../')
from log import write_log


def mod_image(image:netpbm.Netpbm, k:int) -> netpbm.Netpbm:
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
for file_name, k in pieces:
    then = time.time()
    name = "%s_mod_%d" % (file_name, k)
    netpbm.convert_from_p6('%s.pbm' % (file_name))
    image = netpbm.read('%s.pgm' % (file_name))
    image = mod_image(image, k)
    image = netpbm.enlarge(image, ceil(1000 / max(image.M.shape)))
    netpbm.write('%s.pgm' % (name), image)

    t = time.time() - then
    size = os.stat('%s.pgm' % (name)).st_size
    log.append({'name':'%s.pgm' % (name), 't':'%.3f' % t, 'size':size})

# animations

pieces = [('faces',1,150)]      # photo taken by Ella Clemons (3/7/2021)

for file_name, lb, ub in pieces:
    if not os.path.isdir('%s' % file_name):
        os.mkdir('%s' % file_name)
    then = time.time()
    for k in range(lb,ub+1):
        name = "%s_mod_%s" % (file_name, str(k).zfill(3))
        netpbm.convert_from_p6('%s.pbm' % (file_name))
        image = netpbm.read('%s.pgm' % (file_name))
        image = mod_image(image, k)
        netpbm.write('%s/%s.pgm' % (file_name, name), image)

    t = time.time() - then
    size = sum(d.stat().st_size for d in os.scandir('%s' % (file_name)))
    log.append({'name':'%s' % (file_name), 't':'%.3f' % t, 'size':size})

write_log('mod.log', log)