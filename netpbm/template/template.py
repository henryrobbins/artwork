import numpy as np

import os
import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)
from netpbm import netpbm
from log import write_log, collapse_log


def template(image:netpbm.Netpbm) -> netpbm.Netpbm:
    """TODO: Add description

    Args:
        image (netpbm.Netpbm): Netpbm image.

    Returns:
        netpbm.Netpbm: TODO: Add description
    """
    # TODO: Implement something new!
    return image


# COMPILE PIECES | XXXX-XX-XX

pieces = [('beebe_trail')]

log = []
for name in pieces:
    file_path = "%s/%s_template.pgm" % (SOURCE_DIR, name)
    ppm_path = '%s/%s.ppm' % (SOURCE_DIR, name)
    file_log = netpbm.transform(in_path=ppm_path, out_path=file_path,
                                magic_number=2, f=template, scale=1000)
    log.append(file_log)

write_log('%s/%s' % (SOURCE_DIR, 'template.log'), log)
