import numpy as np
import imageio
from numpy import pi
import time

import os
import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)
from log import Log, write_log
from netpbm import colorspace
from animation.animation import clip, transform, pad_to_16


def mod(M,k):
    return np.array(list(map(lambda x: x % k, M)))*int(256/64)


def clip_gradient(M,lb,ub):
    M_lb = np.where(lb <= M, 1, 0)
    M_ub = np.where(M <= ub, 1, 0)
    return np.where(M_lb + M_ub == 2, 0, 255)


def channel(M,f_1,f_2,f_3,color_space):
    if color_space == 'RGB':
        M = colorspace.normalize(M, 'RGB', True)
        M = colorspace.apply_to_channels(M, f_1, f_2, f_3)
        M = colorspace.normalize(M, 'RGB', False)
    elif color_space == 'YUV':
        M = colorspace.RGB_to_YUV(M)
        M = colorspace.normalize(M, 'YUV', True)
        M = colorspace.apply_to_channels(M, f_1, f_2, f_3)
        M = colorspace.normalize(M, 'YUV', False)
        M = colorspace.YUV_to_RGB(M)
    elif color_space == 'Lab':
        M = colorspace.RGB_to_Lab(M)
        M = colorspace.normalize(M, 'Lab', True)
        M = colorspace.apply_to_channels(M, f_1, f_2, f_3)
        M = colorspace.normalize(M, 'Lab', False)
        M = colorspace.Lab_to_RGB(M)
    else:
        raise ValueError("Invalid color space.")
    return M


# COMPILE PIECES | 2021-04-14

animations = []

frames = (clip("%s/car_ride" % SOURCE_DIR) +
          clip("%s/pinches" % SOURCE_DIR) +
          clip("%s/henry_movement" % SOURCE_DIR) +
          clip("%s/ella_movement" % SOURCE_DIR) +
          clip("%s/destroy_town" % SOURCE_DIR))

# TODO: Check these out:
# https://vimeo.com/197136070
# https://www.youtube.com/watch?v=Yt3nDgnC7M8
# pixel vision fisher-price
# https://en.wikipedia.org/wiki/Sadie_Benning
# the sacrifice 1986 film final scene

animations.append((transform(frames,mod,True,k=64), 'mod'))
animations.append((transform(frames,clip_gradient,True,lb=0,ub=100), 'clip'))

f_1 = lambda x: abs(np.sin(x*5))
f_2 = lambda x: abs((2*12*np.arcsin(np.sin((2*pi*x)/(5))))/(pi))
f_3 = lambda x: 1 - x
animations.append((transform(frames,channel,False,f_1=f_1,f_2=f_2,f_3=f_3,
                   color_space="RGB"), 'rgb_chaos'))

f_1 = lambda p: lambda x: abs(np.sin(x*p))
f_2 = lambda a,p: lambda x: abs((2*a*np.arcsin(np.sin((2*pi*x)/(p))))/(pi))
f_3 = lambda x: 1 - x
frames = (transform(clip("%s/pinches" % SOURCE_DIR,1,5),
            channel,f_1=f_1(5),f_2=f_2(12,5),f_3=f_3,color_space="RGB") +
          transform(clip("%s/pinches" % SOURCE_DIR,6,10),mod,True,k=64) +
          transform(clip("%s/pinches" % SOURCE_DIR,11,14),
            channel,f_1=f_1(8),f_2=f_2(12,5),f_3=f_3,color_space="RGB") +
          transform(clip("%s/pinches" % SOURCE_DIR,15,18),
            channel,f_1=f_1(5),f_2=f_2(12,8),f_3=f_3,color_space="RGB") +
          transform(clip("%s/pinches" % SOURCE_DIR,19,22),
            channel,f_1=f_1(5),f_2=f_2(12,5),f_3=f_3,color_space="RGB") +
          transform(clip("%s/pinches" % SOURCE_DIR,23,28),clip_gradient,True,lb=0,ub=100) +
          transform(clip("%s/pinches" % SOURCE_DIR,29,35),
            channel,f_1=f_1(76),f_2=f_2(7,5),f_3=f_3,color_space="RGB") +
          transform(clip("%s/pinches" % SOURCE_DIR,36,40),
            channel,f_1=f_1(5),f_2=f_2(12,5),f_3=f_3,color_space="RGB") +
          transform(clip("%s/pinches" % SOURCE_DIR,41,45),
            channel,f_1=f_1(3),f_2=f_2(12,5),f_3=f_3,color_space="RGB") +
          transform(clip("%s/pinches" % SOURCE_DIR,46,49),mod,True,k=64) +
          transform(clip("%s/pinches" % SOURCE_DIR,50,53),
            channel,f_1=f_1(0),f_2=f_2(16,5),f_3=f_3,color_space="RGB") +
          transform(clip("%s/pinches" % SOURCE_DIR,54,57),
            channel,f_1=f_1(5),f_2=f_2(12,9),f_3=f_3,color_space="RGB") +
          transform(clip("%s/pinches" % SOURCE_DIR,58,61),clip_gradient,True,lb=0,ub=100) +
          transform(clip("%s/pinches" % SOURCE_DIR,62,66),
            channel,f_1=f_1(5),f_2=f_2(1,5),f_3=f_3,color_space="RGB"))
animations.append((frames,'pinches_chaos'))

log = []
for frames, name in animations:
    then = time.time()
    path = "%s/stewart_%s.mp4" % (SOURCE_DIR, name)
    imageio.mimwrite(uri=path,
                     ims=[pad_to_16(f) for f in frames],
                     format='FFMPEG',
                     fps=16,
                     output_params=["-vf","scale=iw*2:ih*2",
                                    "-sws_flags", "neighbor"])
    now = time.time()
    name = path.split('/')[-1]
    size = os.stat(path).st_size
    log.append(Log(name, now-then, size))

write_log('%s/%s' % (SOURCE_DIR, 'stewart.log'), log)
