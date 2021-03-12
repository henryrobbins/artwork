import os
import time
import numpy as np
from collections import namedtuple
from typing import Tuple, Callable

Netpbm = namedtuple('Netpbm', ['w', 'h', 'k', 'M'])
Netpbm.__doc__ = '''\
Netpbm image.

- w (int): Width of the netpbm image.
- h (int): Height of the netpbm image.
- k (int): Maximum value of gradients.
- M (np.ndarray): h by w NumPy matrix of pixels.'''

def convert_from_p6(file:str):
    """Convert a netpbm file in P6 format to P2 format.

    Args:
        file_name (str): Name of the file to convert.
    """
    file_name = file.split('.')[0]
    file_ext = file.split('.')[-1]
    assert file_ext == 'pbm'
    os.system("convert %s -compress none %s" % (file, file_name + '.pgm'))


def read(file_name:str) -> Netpbm:
    """Read the Netpbm file and return a NumPy matrix.

    Args:
        file_name (str): Name of the Netpbm file.

    Returns:
        Netpbm: Netpbm image.
    """
    lines = open(file_name).readlines()
    assert lines[0][:-1] == 'P2'
    w,h = [int(i) for i in lines[1][:-1].split(' ')]
    k = int(lines[2][:-1])
    M = np.array([line.strip('\n ').split(' ') for line in lines[3:]])
    M = M.astype(int)
    assert (h,w) == M.shape
    return Netpbm(w=w, h=h, k=k, M=M)


def write(file_name:str, image:Netpbm):
    """Write the Netpbm file given the associated matrix of nunbers.

    Args:
        file_name (str): Name of the Netpbm file to be written.
        image (Netpbm): Netpbm image to write.
    """
    f = open(file_name, "w")
    f.write('P2\n')
    f.write("%s %s\n" % (image.w, image.h))
    f.write("%s\n" % (image.k))
    f.write('\n'.join([' '.join(line) for line in image.M.astype(str).tolist()]))
    f.write('\n')
    f.close()


def enlarge(image:Netpbm, k:int) -> Netpbm:
    """Enlarge the netpbm image by the multiplier k.

    Args:
        image (Netpbm): Netpbm image to enlarge.

    Returns:
       Netpbm: Enlarged Netpbm image.
    """
    n,m = image.M.shape
    expanded_rows = np.zeros((n*k,m))
    for i in range(n*k):
        expanded_rows[i] = image.M[i // k]
    expanded = np.zeros((n*k, m*k))
    for j in range(m*k):
        expanded[:,j] = expanded_rows[:,j // k]
    M_prime = expanded.astype(int)
    h,w = M_prime.shape
    return Netpbm(w=w, h=h, k=image.k, M=M_prime)


def change_gradient(image:Netpbm, k:int) -> Netpbm:
    """Change the max gradient value of the netpbm image M to n.

    Args:
        image (Netpbm): Netpbm image to change gradient for.
        k (int): New max gradient value.

    Returns:
       Netpbm: Netpbm image with changed gradient.
    """
    M_prime = np.array(list(map(lambda x: x // int(image.k / k), image.M)))
    return Netpbm(w=image.w, h=image.h, k=k, M=M_prime)


# def compile(path:str, pbm_path:str, f:Callable, scale:int=-1, **kwargs) -> Tuple:
#     """Write the netpbm image from path_pbm after applying function f to it.

#     Args:
#         path (str): Path the netpbm image should be written to.
#         pbm_path (str): Path of the pbm image.
#         f (Callable): Function to apply to the netpbm image.
#         scale (int): Desired dimension (Defaults to -1: no desired dimension).

#     Returns:
#         Tuple: name of created file, time to compile, and size of file.
#     """
#     then = time.time()
#     netpbm.convert_from_p6(pbm_path)
#     pgm_path = pbm_path[:-3] + '.pgm'
#     M, w, h, n = netpbm.read(pgm_path)
#     M_prime = f(M=M, **kwargs)
#     if scale != -1:
#         M_prime = netpbm.enlarge(M_prime, ceil(scale / max(M_prime.shape)))
#     netpbm.write(path, M_prime, k)





#     if not os.path.exists(path):
#         os.makedirs(path)

