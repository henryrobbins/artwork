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


def shift(frames, shift):
    tmp = []
    skip = shift
    for frame in frames:
        b = skip % 255
        tmp.append(np.hstack((frame[:,b:,:],frame[:,:b,:])))
        skip += shift
    return tmp


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


plate_frames = transform(clip("%s/plate" % SOURCE_DIR),
               channel,f1=lambda x: x,f2=lambda x: 0.55,f3=lambda x: 0.6,
               color_space='Lab')
frames = (
    [np.zeros((189,255,3))]*10 +
    shift(transform(clip("%s/town_tour" % SOURCE_DIR),
            channel, f1=f3(), f2=f3(), f3=f3(), color_space='RGB'), 1) +
    transform(clip("%s/pinches" % SOURCE_DIR, 29, 35),
            mod, True, k=64) +
    shift(transform(clip("%s/henry_movement" % SOURCE_DIR),
            clip_gradient, True, lb=100, ub=200), 20) +
    transform(clip("%s/pinches" % SOURCE_DIR, 36, 40),
            channel, f1=f1(0), f2=f2(16,5), f3=f3(), color_space='RGB') +
    shift(transform(clip("%s/ella_movement" % SOURCE_DIR),
            clip_gradient, True, lb=100, ub=200), 20) +
    shift(transform(clip("%s/destroy_town" % SOURCE_DIR, 1, 19),
            channel, f1=f3(), f2=f3(), f3=f3(), color_space='RGB'), 1) +
    transform(clip("%s/pinches" % SOURCE_DIR, 1, 5),
                clip_gradient,True,lb=100,ub=200) +
    shift(transform(clip("%s/destroy_town" % SOURCE_DIR, 19, 44)[::-1],
              channel, f1=f3(), f2=f3(), f3=f3(), color_space='RGB'), -5) +
    transform(clip("%s/pinches" % SOURCE_DIR, 41, 45),
              channel,f1=lambda x: x,f2=lambda x: 0.5,f3=lambda x: 0.6,
              color_space='Lab') +
    shift(transform(clip("%s/destroy_town" % SOURCE_DIR, 19, 44),
              mod, True, k=64), 5) +
    transform(clip("%s/pinches" % SOURCE_DIR, 50, 53),
              mod, True, k=32) +
    shift(plate_frames[15:29][::-1] +
          plate_frames[15:] +
          plate_frames[24:29][::-1] +
          plate_frames[24:], 8) +
    transform(clip("%s/pinches" % SOURCE_DIR, 23, 28),
              clip_gradient, True, lb=0, ub=100) +
    shift(transform(clip("%s/tree_flowers" % SOURCE_DIR, 5, 22),
              channel, f1=f3(), f2=f3(), f3=f3(), color_space='RGB'), 10) +
    shift(transform(clip("%s/tree_flowers" % SOURCE_DIR, 5, 22)[::-1],
          channel, f1=f3(), f2=f3(), f3=f3(), color_space='RGB'), -10) +
    transform(clip("%s/pinches" % SOURCE_DIR, 11, 14),
        channel,f1=lambda x: x,f2=lambda x: 0.55,f3=lambda x: 0.6,
               color_space='Lab') +
    [np.zeros((189,255,3))]*10
)
animations.append((frames,'film'))

log = []
for frames, name in animations:
    path = "%s/stewart_%s.mp4" % (SOURCE_DIR, name)
    log.append(animation(frames=frames, path=path, fps=14, s=6))

write_log('%s/%s' % (SOURCE_DIR, 'stewart.log'), log)
