import imageio
import numpy as np
from math import ceil
from skimage.color import rgb2gray, gray2rgb
from typing import List, Callable

import os
import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)


def clip(path:str, start:int = None, end:int = None) -> List[np.ndarray]:
    """Return a list of images in the given directory at the path.

    Args:
        path (str): Path to directory containing image files.
        start (int, optional): Starting frame. Defaults to None.
        end (int, optional): Ending frame. Defaults to None.

    Returns:
        List[np.ndarray]: List of NumPy arrays representing images.
    """
    def listdir_nohidden(path):
        for f in os.listdir(path):
            if not f.startswith('.'):
                yield f

    files = sorted(listdir_nohidden(path))
    if start is not None and end is not None:
        files = files[start-1:end]
    paths = ["%s/%s" % (path, f) for f in files]
    frames = [imageio.imread(path) for path in paths]
    return frames


def transform(frames:List[np.ndarray],
              f:Callable,
              greyscale:bool = False, **kwargs) -> List[np.ndarray]:
    """Transform the frames using the provided function.

    Args:
        frames (List[np.ndarray]): List of images.
        f (Callable): Function to apply to each image in frames.
        greyscale (bool): True if frames are greyscale. Defaults to False.

    Returns:
        List[np.ndarray]: List of transformed images.
    """
    tmp = list(frames)
    for i in range(len(tmp)):
        M = tmp[i]
        if greyscale:
            M = rgb2gray(M)*255
            M = f(M,**kwargs)
        else:
            n,m,_ = M.shape
            M = M.reshape(n,3*m)
            M = f(M,**kwargs)
            M = M.reshape(n,m,3)
        if greyscale:
            M = gray2rgb(M)
        M = M.astype(np.uint8).clip(0,255)
        tmp[i] = M
    return tmp


def pad_to_16(M:np.ndarray) -> np.ndarray:
    """Return M padded such that dimensions are multiples of 16."""
    # Adapted from code by: https://stackoverflow.com/users/9698684/yatu
    m,n,_ = M.shape
    y_pad = (ceil(m/16)*16-m)
    x_pad = (ceil(n/16)*16-n)
    return np.pad(M,((y_pad // 2, y_pad // 2 + y_pad % 2),
                     (x_pad // 2, x_pad // 2 + x_pad % 2),
                     (0,0)))
