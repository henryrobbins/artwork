from os import terminal_size
from dmtools import netpbm
import logging
logging.basicConfig(filename='template.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')


def template(image:netpbm.Netpbm) -> netpbm.Netpbm:
    """TODO: Add description

    Args:
        image (netpbm.Netpbm): Netpbm image.

    Returns:
        netpbm.Netpbm: TODO: Add description
    """
    # TODO: Implement an interesting transformation!
    return image


# COMPILE PIECES | XXXX-XX-XX

pieces = [('beebe_trail')]

works = []
for name in pieces:
    image = netpbm.read_netpbm('%s.ppm' % name)
    image = template(image)
    path = "%s_template.pgm" % name
    image.to_netpbm(path)
    works.append(path)

# TODO: uncomment this
# with open("works.txt", "w") as f:
#     for work in works:
#         f.write("%s\n" % work)
