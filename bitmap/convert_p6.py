import os
import sys
import numpy as np

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
lines = open(file_name).readlines()
assert lines[0][:-1] == 'P2'
w,h = [int(i) for i in lines[1][:-1].split(' ')]
assert int(lines[2][:-1]) == 255
pic = np.array([line.strip('\n ').split(' ') for line in lines[3:]]).astype(int)
assert (h,w) == pic.shape

# map current numbers to desired gradient
new_pic = np.array(list(map(lambda x: x // int(255/n), pic)))
assert np.max(new_pic) <= n

# write the new image file
f = open(file_name, "w")
f.write('P2\n')
f.write("%s %s\n" % (w, h))
f.write("%s\n" % (n))
f.write('\n'.join([' '.join(line) for line in new_pic.astype(str).tolist()]))
f.write('\n')
f.close()
