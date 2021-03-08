import os
import sys
import numpy as np
import netpbm

# Currently only maps to P2 for some number of gradients
# TODO: Allow for mapping to P3 as well

# get arguments
args = sys.argv
file = args[1]
file_name = file.split('.')[0] + ".pgm"
file_ext = file.split('.')[-1]
assert file_ext == 'pbm'
n = int(args[2])  # number of gradients

# convert to P3 format
os.system("convert %s -compress none %s" % (file, file_name))

# parse the P3 image file
pic, w, h, max_val = netpbm.read(file_name)

# map current numbers to desired gradient
new_pic = np.array(list(map(lambda x: x // int(255/n), pic)))
assert np.max(new_pic) <= n

# write the new image file
netpbm.write(file_name, new_pic, n)
