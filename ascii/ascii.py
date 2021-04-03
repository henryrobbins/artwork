import numpy as np
from collections import namedtuple

import os
import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(SOURCE_DIR)
sys.path.insert(0,root)
from netpbm import netpbm

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


def write(ascii:Ascii, path:str):
    """Write the Ascii art to the given path.

    Args:
        ascii (Ascii): Ascii art object.
        path (str): Path to write the ascii art to.
    """
    with open(path, "w") as f:
        lines = ascii.M.astype(str).tolist()
        f.write('\n'.join([' '.join(line) for line in lines]))
        f.write('\n')
