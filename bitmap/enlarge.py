import os
import sys
import numpy as np


# get arguments
args = sys.argv
file_name = args[1]
k = int(args[2])  # how much to enlarge this image by


# parse the P3 image file
lines = open(file_name).readlines()
if lines[0][:-1] != 'P2': 
    raise ValueError("Must be a .pgm file with header P2.")
w,h = [int(i) for i in lines[1][:-1].split(' ')]
n = int(lines[2][:-1])
pic = np.array([line.strip('\n ').split(' ') for line in lines[3:]]).astype(int)
if (h,w) != pic.shape: 
    raise ValueError("Dimensions given do not match the actual.")
    
def expand(array, k):
    """Expand some numpy array by the multiplier k."""
    n,m = array.shape
    expanded_rows = np.zeros((n*k,m))
    for i in range(n*k):
        expanded_rows[i] = array[i // k]
    expanded = np.zeros((n*k, m*k))
    for j in range(m*k):
        expanded[:,j] = expanded_rows[:,j // k]
    return expanded

new_pic = expand(pic, k).astype(int)
    
# write the new image file
f = open(file_name, "w")
f.write('P2\n')
h,w = new_pic.shape
f.write("%s %s\n" % (w, h))
f.write("%s\n" % (n))
f.write('\n'.join([' '.join(line) for line in new_pic.astype(str).tolist()]))
f.close()
