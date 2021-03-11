import os
import sys
import netpbm

# Currently only maps to P2 for some number of gradients
# TODO: Allow for mapping to P3 as well

# get arguments
args = sys.argv
file = args[1]
file_name = file.split('.')[0] + ".pgm"
file_ext = file.split('.')[-1]
assert file_ext == 'pbm'

# convert to P3 format
os.system("convert %s -compress none %s" % (file, file_name))
