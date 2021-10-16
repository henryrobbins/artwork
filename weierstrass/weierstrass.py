import dmtools
from dmtools import transform, animation
import numpy as np
import logging
logging.basicConfig(filename='clip.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')

# COMPILE PIECES | 2021-XX-XX

def weierstrass(x, a, b):
    return sum(a**n*np.cos(b**n*np.pi*x) for n in range(100))

def f(x):
    # return np.sin(np.pi*x + (np.pi/2))
    return weierstrass(x, 0.5, 3)


image = dmtools.read_png("sunset.png")
image = transform.rescale(image, k=0.2, filter="triangle")
# image = transform.blur(image, 2)

# --------------
# single image

image = transform.rescale(image, k=0.5, weighting_function=f, support=20)
image = transform.wraparound(image).astype(np.uint8)

image = transform.rescale(image, k=4, filter="point")
image = transform.clip(image).astype(np.uint8)

dmtools.write_png(image, "test_w_2.png")
# --------------


# --------------
# animation

# frames = []
# for i in np.linspace(1,10,10):
#     # f = lambda x: weierstrass(x, 0.5, i)
#     frame = transform.rescale(image, k=0.25, weighting_function=f, support=((np.pi*i)/2))
#     frame = transform.wraparound(frame).astype(np.uint8)
#     frame = transform.rescale(frame, k=4, filter="point")
#     frame = transform.clip(frame).astype(np.uint8)
#     frames.append(frame)

# animation.to_mp4(frames=frames, path="test4.mp4", fps=10)
# --------------


# --------------
# tree_shift.mp4
# --------------

# image = dmtools.read_png("trees_sunset.png")
# image = transform.rescale(image, k=0.25, filter="triangle")

# frames = []
# for i in np.linspace(1,120,60):
#     f = lambda x: 1 if int(x) == int(i/2) else 0
#     frame = transform.rescale(image, k=0.5, weighting_function=f, support=i)
#     frame = transform.wraparound(frame).astype(np.uint8)
#     frames.append(frame)

# animation.to_mp4(frames=frames, path="test.mp4", fps=10)


# --------------------
# tree_<x>_<clamp>.png
# --------------------m
# image = dmtools.read_png("sunset.png")
# image = transform.rescale(image, k=0.25, filter="triangle")

# image = transform.rescale(image, k=0.5, weighting_function=f, support=20)
# image = transform.normalize(image).astype(np.uint8)

# image = transform.rescale(image, k=4, filter="point")
# image = transform.clip(image).astype(np.uint8)

# dmtools.write_png(image, "tree_20_normalize.png")
