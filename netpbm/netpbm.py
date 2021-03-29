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

# Dictionary from Netpbm extentsions to magic number and vice versa
EXT_TO_MAGIC = {"pbm":1, "pgm":2, "ppm":3}
MAGIC_TO_EXT = {1:"pbm", 2:"pgm", 3:"ppm"}

Netpbm = namedtuple('Netpbm', ['P', 'w', 'h', 'k', 'M'])
Netpbm.__doc__ = '''\
Netpbm image.

- P (int): "Magic number" of the Netpbm image {1,2,3}.
- w (int): Width of the netpbm image.
- h (int): Height of the netpbm image.
- k (int): Maximum value of gradients.
- M (np.ndarray): h by w NumPy matrix of pixels.'''

def raw_to_plain(path:str, magic_number:int=None) -> str:
    """Convert a netpbm file in raw format to plain format.

    Args:
        path (str): Path to the file to convert.
        magic_number (int): "Magic number" {1,2,3}.

    Return:
        str: Path to the resulting file.
    """
    prev = EXT_TO_MAGIC[path[-3:]]
    magic_number = prev if magic_number is None else magic_number
    assert magic_number <= prev
    if magic_number == prev:
        out_path = path[:-4] + "_plain." + MAGIC_TO_EXT[magic_number]
    else:
        out_path = path[:-3] + MAGIC_TO_EXT[magic_number]
    os.system("convert %s -compress none %s" % (path, out_path))
    return out_path


def read(file_name:str) -> Netpbm:
    """Read the Netpbm file and return a NumPy matrix.

    Args:
        file_name (str): Name of the Netpbm file.

    Returns:
        Netpbm: Netpbm image.
    """
    # Adapted from code provided by Dan Torop
    with open(file_name) as f:
        vals = [v for line in f for v in line.split('#')[0].split()]
        P = int(vals[0][1])
        w, h, k, *vals = [int(v) for v in vals[1:]]
        is_P3 = (3 if P == 3  else 1)
        assert len(vals) == w * h * is_P3
        M = np.array(vals).reshape(h, w * is_P3)
        return Netpbm(P=P, w=w, h=h, k=k, M=M)


def write(file_name:str, image:Netpbm):
    """Write the Netpbm file given the associated matrix of nunbers.

    Args:
        file_name (str): Name of the Netpbm file to be written.
        image (Netpbm): Netpbm image to write.
    """
    with open(file_name, "w") as f:
        f.write('P%d\n' % image.P)
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
    if image.P == 3:
        for j in range(int(m/3)*k):
            x = (j // k) * 3
            y = j * 3
            expanded[:,y:y+3] = expanded_rows[:,x:x+3]
    else:
        for j in range(m*k):
            expanded[:,j] = expanded_rows[:,j // k]
    M_prime = expanded.astype(int)
    w,h = image.w, image.h
    return Netpbm(P=image.P, w=w*k, h=h*k, k=image.k, M=M_prime)


def change_gradient(image:Netpbm, k:int) -> Netpbm:
    """Change the max gradient value of the netpbm image M to n.

    Args:
        image (Netpbm): Netpbm image to change gradient for.
        k (int): New max gradient value.

    Returns:
       Netpbm: Netpbm image with changed gradient.
    """
    M_prime = np.array(list(map(lambda x: x // int(image.k / k), image.M)))
    return Netpbm(P=image.P, w=image.w, h=image.h, k=k, M=M_prime)


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
    return Netpbm(P= images[0].P,
                  w=w*m + (w+1)*b,
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


def transform(in_path:str, out_path:str, f:Callable, scale:int=-1,
              magic_number=None, **kwargs) -> Log:
    """Apply f to the image at in_path and write result to out_path.

    Args:
        in_path (str): Path of the image to be transformed.
        out_path (str): Path the transformed image is written to.
        f (Callable): Function to apply to the netpbm image.
        scale (int): Scale the image to this dimension. Defaults to -1.
        magic_number (int): "Magic number" {1,2,3}. Defaults to None.

    Returns:
        Log: log from compiling this file.
    """
    then = time.time()

    image = read(raw_to_plain(in_path, magic_number=magic_number))
    new_image = f(image=image, **kwargs)
    if scale != -1:
        m = ceil(scale / max(new_image.w,new_image.h))
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
