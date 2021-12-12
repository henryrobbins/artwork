import os
import numpy as np
from numpy import pi
from scipy import signal
from dmtools import colorspace, adjustments
from dmtools.animation import clip, to_mp4
from dmtools import sound
import logging
logging.basicConfig(filename='stewart.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')

def mod(M,k):
    M = colorspace.RGB_to_gray(M)
    M = np.array(list(map(lambda x: x % k, M)))*int(256/k)
    return colorspace.gray_to_RGB(M)


def clip_gradient(M,lb,ub):
    M = colorspace.RGB_to_gray(M)
    M_lb = np.where(lb / 255 <= M, 1, 0)
    M_ub = np.where(M <= ub / 255, 1, 0)
    M = np.where(M_lb + M_ub == 2, 0, 1)
    return colorspace.gray_to_RGB(M)


def channel(M,f1,f2,f3,color_space='RGB'):
    if color_space == 'RGB':
        M = colorspace.normalize(M, 'RGB')
        M = adjustments.apply_curve(M, f1, 0)
        M = adjustments.apply_curve(M, f2, 1)
        M = adjustments.apply_curve(M, f3, 2)
        M = colorspace.denormalize(M, 'RGB')
    elif color_space == 'YUV':
        M = colorspace.RGB_to_YUV(M)
        M = colorspace.normalize(M, 'YUV')
        M = adjustments.apply_curve(M, f1, 0)
        M = adjustments.apply_curve(M, f2, 1)
        M = adjustments.apply_curve(M, f3, 2)
        M = colorspace.denormalize(M, 'YUV')
        M = colorspace.YUV_to_RGB(M)
    elif color_space == 'Lab':
        M = colorspace.RGB_to_Lab(M)
        M = colorspace.normalize(M, 'Lab')
        M = adjustments.apply_curve(M, f1, 0)
        M = adjustments.apply_curve(M, f2, 1)
        M = adjustments.apply_curve(M, f3, 2)
        M = colorspace.denormalize(M, 'Lab')
        M = colorspace.Lab_to_RGB(M)
    else:
        raise ValueError("Invalid color space.")
    return M

def shift(frames, shift):
    tmp = []
    skip = shift
    for frame in frames:
        b = skip % 255
        if len(frame.shape) == 2:
            tmp.append(np.hstack((frame[:,b:],frame[:,:b])))
        else:
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

frames = (clip("input/car_ride") +
          clip("input/pinches") +
          clip("input/henry_movement") +
          clip("input/ella_movement") +
          clip("input/destroy_town"))

# animations.append(([mod(f,64) for f in frames], 'mod', None, None))
animations.append(([clip_gradient(f,0,100) for f in frames], 'clip', None, None))

def f1(p):
    return lambda x: abs(np.sin(x*p))


def f2(a,p):
    return lambda x: abs((2*a*np.arcsin(np.sin((2*pi*x)/(p))))/(pi))


def f3():
    return lambda x: 1 - x

animations.append(([channel(f,f1(5),f2(12,5),f3=f3()) for f in frames], 'rgb_chaos', None, None))


pinches_clip = clip("input/pinches")
b = [0,5,10,14,18,22,28,35,40,45,49,53,57,61,66]
clips = [pinches_clip[b[i]+1:b[i+1]] for i in range(len(b)-1)]
frames = ([channel(f, f1(5), f2(12,5), f3()) for f in clips[0]] +
          [mod(f, 64) for f in clips[1]] +
          [channel(f, f1(8), f2(12,5),f3()) for f in clips[2]] +
          [channel(f, f1(5), f2(12,8),f3()) for f in clips[3]] +
          [channel(f, f1(5), f2(12,5),f3()) for f in clips[4]] +
          [clip_gradient(f, 0, 100) for f in clips[5]] +
          [channel(f, f1(76), f2(7,5),f3()) for f in clips[6]] +
          [channel(f, f1(5), f2(12,5),f3()) for f in clips[7]] +
          [channel(f, f1(3), f2(12,5),f3()) for f in clips[8]] +
          [mod(f, 64) for f in clips[9]] +
          [channel(f, f1(0), f2(16,5),f3()) for f in clips[10]] +
          [channel(f, f1(5), f2(12,9),f3()) for f in clips[11]] +
          [clip_gradient(f, 0, 100) for f in clips[12]] +
          [channel(f, f1(5), f2(1,5), f3()) for f in clips[13]])
animations.append((frames,'pinches_chaos',None,None))


plate_frames = [channel(f,lambda x: x,lambda x: 0.55, lambda x: 0.6, 'Lab')
                for f in clip("input/plate")]
frames = (
    [np.zeros((189,255,3))]*10 +
    shift([channel(f,f3(),f3(),f3()) for f in clip("input/town_tour")], 1) +
    [mod(f,64) for f in clip("input/pinches", 29, 35)] +
    shift([clip_gradient(f,100,200) for f in clip("input/henry_movement")], 20) +
    [channel(f,f1(0),f2(16,5),f3()) for f in clip("input/pinches", 35, 40)] +
    shift([clip_gradient(f,100,200) for f in clip("input/ella_movement")], 20) +
    shift([channel(f,f3(),f3(),f3()) for f in clip("input/destroy_town", 0, 19)], 1) +
    [clip_gradient(f,100,200) for f in clip("input/pinches", 0, 5)] +
    shift([channel(f,f3(),f3(),f3()) for f in clip("input/destroy_town", 18, 44)[::-1]], -5) +
    [channel(f,lambda x: x,lambda x: 0.5, lambda x: 0.6, 'Lab')
        for f in clip("input/pinches", 40, 45)] +
    shift([mod(f,64) for f in clip("input/destroy_town", 18, 44)], 5) +
    [mod(f,32) for f in clip("input/pinches", 49, 53)] +
    shift(plate_frames[15:29][::-1] +
        plate_frames[15:] +
        plate_frames[24:29][::-1] +
        plate_frames[24:], 8) +
    [clip_gradient(f,0,100) for f in clip("input/pinches", 22, 28)] +
    shift([channel(f,f3(),f3(),f3()) for f in clip("input/tree_flowers", 4, 22)], 10) +
    shift([channel(f,f3(),f3(),f3()) for f in clip("input/tree_flowers", 4, 22)[::-1]], -10) +
    [channel(f,lambda x: x,lambda x: 0.55, lambda x: 0.6, 'Lab')
        for f in clip("input/pinches", 10, 14)] +
    [np.zeros((189,255,3))]*10
)

# adding sound to stewart_film
fps = 10
t = (len(frames) / fps)

line = np.linspace(0, t*(2*np.pi), int(t*sound.SAMPLE_RATE/25))
avgs = np.repeat([np.average(frame) / 255 for frame in frames],
                 int(sound.SAMPLE_RATE/fps/25))[:len(line)]
line = line[:len(avgs)]
avgs = (avgs * 400 + 100)  # normalize
wave1 = 0.2*np.sin(line*avgs)
wave1 = signal.resample(wave1, 25*len(wave1))

clips = np.repeat([np.average(np.where(f > 180, 1, 0)) for f in frames],
                  int(sound.SAMPLE_RATE/fps/25))[:len(line)]
line = line[:len(clips)]
clips = (clips * 400 + 100)  # normalize
wave2 = 0.4*np.cos(line*avgs)
wave2 = signal.resample(wave2, 25*len(wave2))

wave = wave1 + wave2
wave = wave / np.max(np.absolute(wave))

animations.append((frames, 'film', sound.WAV(r=wave, l=wave), fps))


os.makedirs('output', exist_ok=True)
for frames, name, audio, fps in animations:
    path = "output/stewart_%s.mp4" % name
    to_mp4(frames=frames, audio=audio, path=path, fps=fps, s=3)
