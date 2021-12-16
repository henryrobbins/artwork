import os
import dmtools
from dmtools import transform, animation
from functools import lru_cache
import numpy as np
from assistant.help import get_metadata


# NOTES:
# For scale factor k, the period of samples from weighting function f is
#                  T = (round(0.5 / k) - (0.5 / k)) * k.

def weierstrass(x, a, b):
    return sum(a**n*np.cos(b**n*np.pi*x) for n in range(100))

@lru_cache()
def f(x):
    return weierstrass(x, 0.5, 3)

# --------------
# animation

# frames = []
# for i in np.linspace(1,20,20):
#     # f = lambda x: weierstrass(x, 0.5, i)
#     frame = transform.rescale(image, k=0.5, weighting_function=f, support=i)
#     frame = transform.wraparound(frame).astype(np.uint8)
#     frame = transform.rescale(frame, k=4, filter="point")
#     frame = transform.clip(frame).astype(np.uint8)
#     frames.append(frame)

# animation.to_mp4(frames=frames, path="test7.mp4", fps=10)
# --------------

# COMPILE PIECES | 2021-XX-XX

pieces = [('sunset', 0.5, 3, 0.5, 10),
          ('sunset', 0.5, 3, 0.5, 20),
          ('circuit_1', 0.5, 3, 0.5, 20),
          ('circuit_2', 0.5, 3, 0.5, 20),
          ('circuit_3', 0.5, 3, 0.5, 20)]


os.makedirs('output', exist_ok=True)
for name, a, b, k, support in pieces:
    image = dmtools.read_png("input/%s.png" % name)
    # image = transform.rescale(image, k=0.5, filter="triangle")
    # image = transform.blur(image, 2)

    f = lambda x: weierstrass(x, a, b)
    image = transform.rescale(image, k=k, weighting_function=f, support=support)
    image = np.mod(image, 1)
    image = image[support:-support, support:-support]

    image = transform.rescale(image, k=(1/k), filter="point")
    image = transform.clip(image)

    path = "output/%s_weierstrass_%d.png" % (name, support)
    dmtools.write_png(image, path, metadata=get_metadata())
