import numpy as np
from numpy import pi

import os
import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)
from log import write_log
from netpbm import colorspace
from animation.animation import clip, transform, animation


def mod(M,k):
    return np.array(list(map(lambda x: x % k, M)))*int(256/64)


def clip_gradient(M,lb,ub):
    M_lb = np.where(lb <= M, 1, 0)
    M_ub = np.where(M <= ub, 1, 0)
    return np.where(M_lb + M_ub == 2, 0, 255)


def channel(M,f1,f2,f3,color_space='RGB'):
    if color_space == 'RGB':
        M = colorspace.normalize(M, 'RGB', True)
        M = colorspace.apply_to_channels(M, f1, f2, f3)
        M = colorspace.normalize(M, 'RGB', False)
    elif color_space == 'YUV':
        M = colorspace.RGB_to_YUV(M)
        M = colorspace.normalize(M, 'YUV', True)
        M = colorspace.apply_to_channels(M, f1, f2, f3)
        M = colorspace.normalize(M, 'YUV', False)
        M = colorspace.YUV_to_RGB(M)
    elif color_space == 'Lab':
        M = colorspace.RGB_to_Lab(M)
        M = colorspace.normalize(M, 'Lab', True)
        M = colorspace.apply_to_channels(M, f1, f2, f3)
        M = colorspace.normalize(M, 'Lab', False)
        M = colorspace.Lab_to_RGB(M)
    else:
        raise ValueError("Invalid color space.")
    return M


# TODO: Check these out:
# https://vimeo.com/197136070
# https://www.youtube.com/watch?v=Yt3nDgnC7M8
# pixel vision fisher-price
# https://en.wikipedia.org/wiki/Sadie_Benning
# the sacrifice 1986 film final scene

# COMPILE PIECES | 2021-04-14

animations = []

frames = (clip("%s/car_ride" % SOURCE_DIR) +
          clip("%s/pinches" % SOURCE_DIR) +
          clip("%s/henry_movement" % SOURCE_DIR) +
          clip("%s/ella_movement" % SOURCE_DIR) +
          clip("%s/destroy_town" % SOURCE_DIR))

animations.append((transform(frames,mod,True,k=64), 'mod'))
animations.append((transform(frames,clip_gradient,True,lb=0,ub=100), 'clip'))


def f1(p):
    return lambda x: abs(np.sin(x*p))


def f2(a,p):
    return lambda x: abs((2*a*np.arcsin(np.sin((2*pi*x)/(p))))/(pi))


def f3():
    return lambda x: 1 - x


animations.append((transform(frames, channel,
                             f1=f1(5),f2=f2(12,5),f3=f3()),'rgb_chaos'))


pinches_clip = clip("%s/pinches" % SOURCE_DIR)
b = [0,5,10,14,18,22,28,35,40,45,49,53,57,61,66]
clips = [pinches_clip[b[i]+1:b[i+1]] for i in range(len(b)-1)]
frames = (transform(clips[0],channel,f1=f1(5),f2=f2(12,5),f3=f3()) +
          transform(clips[1],mod,True,k=64) +
          transform(clips[2],channel,f1=f1(8),f2=f2(12,5),f3=f3()) +
          transform(clips[3],channel,f1=f1(5),f2=f2(12,8),f3=f3()) +
          transform(clips[4],channel,f1=f1(5),f2=f2(12,5),f3=f3()) +
          transform(clips[5],clip_gradient,True,lb=0,ub=100) +
          transform(clips[6],channel,f1=f1(76),f2=f2(7,5),f3=f3()) +
          transform(clips[7],channel,f1=f1(5),f2=f2(12,5),f3=f3()) +
          transform(clips[8],channel,f1=f1(3),f2=f2(12,5),f3=f3()) +
          transform(clips[9],mod,True,k=64) +
          transform(clips[10],channel,f1=f1(0),f2=f2(16,5),f3=f3()) +
          transform(clips[11],channel,f1=f1(5),f2=f2(12,9),f3=f3()) +
          transform(clips[12],clip_gradient,True,lb=0,ub=100) +
          transform(clips[13],channel,f1=f1(5),f2=f2(1,5),f3=f3()))
animations.append((frames,'pinches_chaos'))

log = []
for frames, name in animations:
    path = "%s/stewart_%s.mp4" % (SOURCE_DIR, name)
    log.append(animation(frames=frames, path=path, fps=16, s=2))

write_log('%s/%s' % (SOURCE_DIR, 'stewart.log'), log)
