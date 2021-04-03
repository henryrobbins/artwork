import os
import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)
from netpbm import netpbm
from ascii import ascii

path = netpbm.convert_from_p6('%s/%s' % (SOURCE_DIR, 'steal_your_face.pbm'))
image = netpbm.read(path)
image = ascii.netpbm_to_ascii(image)
ascii.write(image, '%s/%s' % (SOURCE_DIR, 'steal_your_face.txt'))
