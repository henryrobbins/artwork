import os
import time
import datetime
import imageio
import numpy as np
from math import ceil
from collections import namedtuple
from skimage.transform import rescale
from typing import List, Callable

import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)
from log import Log


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


def raw_to_plain(path:str, magic_number:int = None) -> str:
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
        if P == 1:
            w, h, *vals = [int(v) for v in vals[1:]]
            k = 1
        else:
            w, h, k, *vals = [int(v) for v in vals[1:]]
        if P == 3:
            M = np.array(vals).reshape(h, w, 3)
        else:
            M = np.array(vals).reshape(h, w)
        return Netpbm(P=P, w=w, h=h, k=k, M=M)


def write(file_name:str, image:Netpbm):
    """Write the Netpbm file given the associated matrix of nunbers.

    Args:
        file_name (str): Name of the Netpbm file to be written.
        image (Netpbm): Netpbm image to write.
    """
    with open(file_name, "w") as f:
        f.write('P%d\n' % image.P)
        comment = netpbm_comment(file_name)
        for line in comment:
            f.write(line)
        f.write("%s %s\n" % (image.w, image.h))
        if image.P != 1:
            f.write("%s\n" % (image.k))
        if image.P == 3:
            M = image.M.reshape(image.h, image.w * 3)
        else:
            M = image.M
        lines = M.clip(0,image.k).astype(int).astype(str).tolist()
        f.write('\n'.join([' '.join(line) for line in lines]))
        f.write('\n')


def write_png(file_name:str, image:Netpbm, size:int):
    """Write the Netpbm file as a PNG file.

    Args:
        file_name (str): Name of the PNG file to be written.
        image (Netpbm): Netpbm image to write.
        size (int): Target width.
    """
    # scale to desired size
    w = image.M.shape[1]
    image = enlarge(image, ceil(size / w))

    # reverse gradient if portable bit map image
    M = image.M
    if image.P == 1:
        M = np.where(M == 1, 0, 1)

    # scale gradient to 255
    M = M * (255 / image.k)
    M = M.astype(np.uint8)

    directory = '/'.join(file_name.split('/')[:-1])
    if not os.path.exists(directory):
        os.makedirs(directory)
    imageio.imwrite(file_name, M)


def enlarge(image:Netpbm, k:int) -> Netpbm:
    """Enlarge the netpbm image by the multiplier k.

    Args:
        image (Netpbm): Netpbm image to enlarge.

    Returns:
       Netpbm: Enlarged Netpbm image.
    """
    # old implementation -- now using skimage for efficency
    # =====================================================
    # M = image.M
    # n,m = M.shape
    # expanded_rows = np.zeros((n*k,m))
    # for i in range(n*k):
    #     expanded_rows[i] = M[i // k]
    # expanded = np.zeros((n*k, m*k))
    # for j in range(m*k):
    #     expanded[:,j] = expanded_rows[:,j // k]
    # M_prime = expanded.astype(int)
    # =====================================================

    # NEAREST_NEIGHBOR (order=0)
    M = rescale(image.M, k,
                order=0, preserve_range=True, multichannel=(image.P == 3))
    w,h = image.w, image.h
    return Netpbm(P=image.P, w=w*k, h=h*k, k=image.k, M=M)


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
               color:int = "white") -> Netpbm:
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
    return Netpbm(P=images[0].P,
                  w=w*m + (w+1)*b,
                  h=h*n + (h+1)*b,
                  k=k, M=grid_layout.astype(int))


def border(image:Netpbm, b:int, color:int = "white") -> Netpbm:
    """Add a border of width b to the image

    Args:
        image (Netpbm): Netpbm image to add a border to
        b (int): width of the border/margin.
        color (int): color of border {'white', 'black'} (defaults to white).

    Returns:
        Netpbm: Image with border added.
    """
    return image_grid([image], w=1, h=1, b=b, color=color)


def transform(in_path:str, out_path:str, f:Callable, scale:int = -1,
              magic_number:int = None, **kwargs) -> Log:
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


def generate(path:str, f:Callable, scale:int = -1, **kwargs) -> Log:
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


def netpbm_comment(file_name:str):
    """Comment to be written in the

    Args:
        file_name (str): Name of the Netpbm file to be written.
    """
    name = file_name.split('/')[-1]
    lines = ["Title: %s\n" % name,
             "Compiled on: %s\n" % datetime.datetime.now(), "\n"]
    readme_path = "/".join(file_name.split('/')[:-1]) + "/README.md"
    with open(readme_path) as f:
        readme = f.readlines()
        indices = [i for i in range(len(readme)) if readme[i] == '\n']
        lines = lines + readme[:indices[1]]
    lines = ["# " + line for line in lines]
    return lines


def animate(pattern:str, out_path:str, fps:int) -> Log:
    """Creates an animation by calling the ffmpeg commmand line tool.

    Args:
        pattern (str): Pattern of the input frame.
        out_path (str): Path to write the output file to.
        fps (int): Frames per second.

    Returns:
        Log: log from compiling this file.
    """
    # -r   set frame rate
    # -i   pattern of image frame file names
    # -y   overwrite output files
    # -an  disable audio
    # -vb  video bitrate
    # -sn  disable subtitle
    then = time.time()
    command = ("ffmpeg -r %d -i %s -y -an -vb 20M -sn %s"
               % (fps, pattern, out_path))
    os.system(command)
    t = time.time() - then
    size = os.stat(out_path).st_size
    name = out_path.split('/')[-1]
    return (Log(name=name, time=t, size=size))
