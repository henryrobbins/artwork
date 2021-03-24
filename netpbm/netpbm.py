import os
import time
import numpy as np
from math import ceil
from collections import namedtuple
from typing import List, Tuple, Callable

import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)
from log import Log, write_log, collapse_log

Netpbm = namedtuple('Netpbm', ['w', 'h', 'k', 'M'])
Netpbm.__doc__ = '''\
Netpbm image.

- w (int): Width of the netpbm image.
- h (int): Height of the netpbm image.
- k (int): Maximum value of gradients.
- M (np.ndarray): h by w NumPy matrix of pixels.'''

def convert_from_p6(path:str) -> str:
    """Convert a netpbm file in P6 format to P2 format.

    Args:
        path (str): Path to the file to convert.

    Return:
        str: Path to the resulting file.
    """
    pgm_path = path[:-3] + 'pgm'
    os.system("convert %s -compress none %s" % (path, pgm_path))
    return pgm_path


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
    with open(file_name, "w") as f:
        f.write('P2\n')
        f.write("%s %s\n" % (image.w, image.h))
        f.write("%s\n" % (image.k))
        lines = image.M.astype(str).tolist()
        f.write('\n'.join([' '.join(line) for line in lines]))
        f.write('\n')


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


def image_grid(images:List[Netpbm], w:int, h:int, b:int,
               color:int="white") -> Netpbm:
    """Create a w * h grid of images with a border of width b.

    Args:
        images (List[Netpbm]): images to be put in the grid (same dimensions).
        w (int): number of images in each row of the grid.
        h (int): number of images in each column of the grid.
        b (int): width of the border/margin.
        color (int): color of border {'white', 'black'} (defaults to white).

    Returns:
        Netpbm: grid layout of the images.
    """
    n,m = images[0].M.shape
    k = images[0].k
    c = {'white':k, 'black':0}[color]
    h_border = c*np.ones((b, w*m + (w+1)*b))
    v_border = c*np.ones((n, b))
    grid_layout = h_border
    p = 0
    for i in range(h):
        row = v_border
        for j in range(w):
            row = np.hstack((row, images[p].M))
            row = np.hstack((row, v_border))
            p += 1
        grid_layout = np.vstack((grid_layout, row))
        grid_layout = np.vstack((grid_layout, h_border))
    return Netpbm(w=w*m + (w+1)*b,
                  h=h*n + (h+1)*b,
                  k=k, M=grid_layout.astype(int))


def border(image:Netpbm, b:int, color:int="white") -> Netpbm:
    """Add a border of width b to the image

    Args:
        image (Netpbm): Netpbm image to add a border to
        b (int): width of the border/margin.
        color (int): color of border {'white', 'black'} (defaults to white).

    Returns:
        Netpbm: Image with border added.
    """
    return image_grid([image], w=1, h=1, b=b, color=color)


def transform(in_path:str, out_path:str, f:Callable,
              scale:int=-1, **kwargs) -> Log:
    """Apply f to the image at in_path and write result to out_path.

    Args:
        in_path (str): Path of the image to be transformed.
        out_path (str): Path the transformed image is written to.
        f (Callable): Function to apply to the netpbm image.
        scale (int): Scale the image to this dimension. Defaults to -1.

    Returns:
        Log: log from compiling this file.
    """
    then = time.time()

    image = read(convert_from_p6(in_path))
    new_image = f(image=image, **kwargs)
    if scale != -1:
        m = ceil(scale / max(new_image.M.shape))
        new_image = enlarge(new_image, m)
    write(out_path, new_image)

    t = time.time() - then
    size = os.stat(out_path).st_size
    name = out_path.split('/')[-1]
    return (Log(name=name, time=t, size=size))


def generate(path:str, f:Callable, scale:int=-1, **kwargs) -> Log:
    """Generate a Netpbm image using f and write the image to the path.

    Args:
        path (str): Path to write the generated Netpbm image to.
        f (Callable): Function used to generate the image.
        scale (int): Scale the image to this dimension. Defaults to -1.

    Returns:
        Log: log from compiling this file.
    """
    then = time.time()

    image = f(**kwargs)
    if scale != -1:
        m = ceil(scale / max(image.M.shape))
        image = enlarge(image, m)
    write(path, image)

    t = time.time() - then
    size = os.stat(path).st_size
    name = path.split('/')[-1]
    return (Log(name=name, time=t, size=size))
