import os
import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)
from netpbm import netpbm
from ascii import ascii
from log import write_log, write_works

path = netpbm.raw_to_plain('%s/%s' % (SOURCE_DIR, 'steal_your_face.ppm'), 2)
image = netpbm.read(path)
image = ascii.netpbm_to_ascii(image)
log = ascii.write(image, '%s/%s' % (SOURCE_DIR, 'steal_your_face.png'), 'png')
logs = [log]

write_log('%s/%s' % (SOURCE_DIR, 'steal_your_face.log'), logs)
write_works(SOURCE_DIR, logs)
