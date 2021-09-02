import os
from dmtools import netpbm, ascii
import logging
logging.basicConfig(filename='steal_your_face.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))

raw_file = '%s/%s' % (SOURCE_DIR, 'steal_your_face.ppm')
plain_file = netpbm.raw_to_plain(raw_file, 2)
netpbm_img = netpbm.read(plain_file)
ascii_img = ascii.netpbm_to_ascii(netpbm_img)
ascii.write(ascii_img, '%s/%s' % (SOURCE_DIR, 'steal_your_face.png'), 'png')

works = ['steal_your_face.png']
with open("works.txt", "w") as f:
    f.writelines(works)
