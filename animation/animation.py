import imageio
import numpy as np
from math import ceil
import time
from skimage.color import rgb2gray, gray2rgb
from typing import List, Callable

import os
import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)
from log import Log
from animation import sound


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
            M = f(M,**kwargs)
        if greyscale:
            M = gray2rgb(M)
        tmp[i] = M
    return tmp


def pad_to_16(M:np.ndarray) -> np.ndarray:
    """Return M padded such that dimensions are multiples of 16."""
    # Adapted from code by: https://stackoverflow.com/users/9698684/yatu
    if len(M.shape) == 3:
        m,n,_ = M.shape
        y_pad = (ceil(m/16)*16-m)
        x_pad = (ceil(n/16)*16-n)
        return np.pad(M,((y_pad // 2, y_pad // 2 + y_pad % 2),
                         (x_pad // 2, x_pad // 2 + x_pad % 2),
                         (0,0)))
    else:
        m,n = M.shape
        y_pad = (ceil(m/16)*16-m)
        x_pad = (ceil(n/16)*16-n)
        return np.pad(M,((y_pad // 2, y_pad // 2 + y_pad % 2),
                         (x_pad // 2, x_pad // 2 + x_pad % 2)))


def animation(frames:List[np.ndarray], path:str, fps:int, s:int = 1,
              audio:sound.WAV=None) -> Log:
    """Write an animation as a .mp4 file using ffmpeg through imageio.mp4

    Args:
        frames (List[np.ndarray]): List of frames in the animation.
        audio (sound.WAV): Audio for the animation (None if no audio).
        path (str): Path where the file should be written.
        fps (int): Frames per second.
        s (int, optional): Multiplier for scaling. Defaults to 1.

    Returns:
        Log: log from writing this animation file.
    """
    then = time.time()
    frames = [f.astype(np.uint8).clip(0,255) for f in frames]
    frames = [pad_to_16(f) for f in frames]
    imageio.mimwrite(uri="tmp.mp4" if audio is not None else path,
                     ims=frames,
                     format='FFMPEG',
                     fps=fps,
                     output_params=["-vf","scale=iw*%d:ih*%d" % (s,s),
                                    "-sws_flags", "neighbor"])
    if audio is not None:
        sound.write("tmp.wav", audio)
        os.system("ffmpeg -i %s -i %s -c:v copy -c:a aac -y %s"
                  % ("tmp.mp4", "tmp.wav", path))
        os.system("rm tmp.mp4")
        os.system("rm tmp.wav")
    now = time.time()
    name = path.split('/')[-1]
    size = os.stat(path).st_size
    return Log(name, now-then, size)
