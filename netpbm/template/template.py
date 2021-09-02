import numpy as np
import os
from dmtools import netpbm
import logging
logging.basicConfig(filename='template.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))

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

works = []
for name in pieces:
    file_path = "%s/%s_template.pgm" % (SOURCE_DIR, name)
    ppm_path = '%s/%s.ppm' % (SOURCE_DIR, name)
    netpbm.transform(in_path=ppm_path, out_path=file_path,
                     magic_number=2, f=template, scale=1000)
    works.append("%s_template.pgm" % name)

# TODO: uncomment this
# with open("works.txt", "w") as f:
#     for work in works:
#         f.write("%s\n" % work)
