import numpy as np
import time
from collections import namedtuple

import os
import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(SOURCE_DIR)
sys.path.insert(0,root)
from netpbm import netpbm
from log import Log

ascii_map = netpbm.read('%s/%s' % (SOURCE_DIR, 'ascii_to_png.pgm'))
img_arrays = [np.pad(M,((0,0),(6,6))) for M in np.split(ascii_map.M,13,axis=1)]
CHAR_TO_IMG = dict(zip(list(" .,-~:;=!*#$@"), img_arrays))

Ascii = namedtuple('Ascii', ['M'])
Ascii.__doc__ = '''\
Ascii image.
- M (np.ndarray): Numpy array of ascii characters.'''


def netpbm_to_ascii(image:netpbm.Netpbm) -> Ascii:
    """Return an ascii representation of the given image."""
    chars = "  -~:;=!*#$@"
    M = netpbm.change_gradient(image, len(chars)-1).M.astype(int)
    M = np.array([[chars[i] for i in row] for row in M])
    return Ascii(M=M)


def write(ascii:Ascii, path:str, type:str):
    """Write the Ascii art to the given path.

    Args:
        ascii (Ascii): Ascii art object.
        path (str): Path to write the ascii art to.
        type (string): {"png", "txt"}
    """
    then = time.time()

    if type == "txt":
        with open(path, "w") as f:
            lines = ascii.M.astype(str).tolist()
            f.write('\n'.join([' '.join(line) for line in lines]))
            f.write('\n')
    else:
        A = np.array([[' ', '$'],['#', ' '],['~', ',']])
        A = ascii.M
        n,m = A.shape
        M = []
        for i in range(n):
            M.append([CHAR_TO_IMG[A[i,j]] for j in range(m)])
        M = np.block(M)
        n,m = M.shape
        image = netpbm.Netpbm(P=2, w=m, h=n, k=255, M=M)
        netpbm.write_png(path, image, 1)

    t = time.time() - then
    size = os.stat(path).st_size
    name = path.split('/')[-1]
    return (Log(name=name, time=t, size=size))
