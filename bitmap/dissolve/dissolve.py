import os
import sys
import numpy as np


# get arguments
args = sys.argv
base_file = args[1]
file_name = args[2]
style = args[3]
i = int(args[4])


# parse the P3 image file
lines = open(base_file).readlines()
if lines[0][:-1] != 'P2': 
    raise ValueError("Must be a .pgm file with header P2.")
w,h = [int(i) for i in lines[1][:-1].split(' ')]
n = int(lines[2][:-1])
pic = np.array([line.strip('\n ').split(' ') for line in lines[3:]]).astype(int)
if (h,w) != pic.shape: 
    raise ValueError("Dimensions given do not match the actual.")
    
if style == 'h':
    if (i < 0) | (i >= h):
        raise ValueError("The given i was out of range.")
elif style == 'v':
    if (i < 0) | (i >= w):
        raise ValueError("The given i was out of range.")
else:
    raise ValueError("'h' for horizontal or 'v' for vertical.")
    
    
def dissolve_iter(v):
    """Return vector v after one iteration of dissolving."""
    n = len(v)
    v_new = []
    for i in range(n):
        l = 0 if i-1 < 0 else v[i-1]
        r = 0 if i+1 >= n else v[i+1]
        x = v[i]
        if x != 0:
            if (x > l) & (x > r):
                x_new = x - 2
            elif (x < l) & (x < r):
                x_new = x + 2
            elif ((x == l) & (x < r)) | ((x == r) & (x < l)):
                x_new = x + 1
            elif ((x == l) & (x > r)) | ((x == r) & (x > l)):
                x_new = x - 1
            else:
                x_new = x
        else:
            x_new = x
        v_new.append(max(0,x_new))
    return np.array(v_new)


def dissolve(v):
    """Return the evolution of v as it dissolves completely."""
    n = len(v)
    v_current = v
    v_hist = [list(v)]
    while len(np.where(v_current != 0 )[0]) > 0:
        v_current = dissolve_iter(v_current)
        v_hist.append(list(v_current))
    return np.array(v_hist)


if style == 'h':
    new_pic = np.vstack((pic[:i], dissolve(pic[i])))
elif style == 'v':
    new_pic = np.hstack((pic[:,:i], dissolve(pic[:,i]).T))
else:
    raise ValueError("'h' for horizontal or 'v' for vertical.")
    
# write the new image file
f = open(file_name, "w")
f.write('P2\n')
h,w = new_pic.shape
f.write("%s %s\n" % (w, h))
f.write("%s\n" % (n))
f.write('\n'.join([' '.join(line) for line in new_pic.astype(str).tolist()]))
f.close()
