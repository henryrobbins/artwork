import os
import numpy as np
import dmtools
from dmtools import transform, colorspace, arrange


def safe_divide(n: np.ndarray, d: np.ndarray) -> np.ndarray:
    return np.divide(n, d, out=np.zeros_like(n), where=(d != 0))


def alpha_composite(aA, aB) -> np.ndarray:
    return np.clip(aA + aB, 0, 1)


def color_composite(xA, aA, xB, aB, xaA, xaB, aR) -> np.ndarray:
    return safe_divide(xaA * transform.normalize(xaB*5), aR)


def f(source:np.ndarray, dest:np.ndarray) -> np.ndarray:
    source = transform.rescale(source, 0.5)
    dest = transform.rescale(dest, 0.5)
    # source = colorspace.add_alpha(source, 0.5)
    # dest = colorspace.add_alpha(dest, 0.5)
    source[:,:,3] = 0.5*source[:,:,3]
    dest[:,:,3] = 0.5*dest[:,:,3]
    # source = colorspace.add_alpha(source, 0.5)

    n,m,*_ = source.shape
    background = np.ones((n,m,3)) * (150 / 255)
    background = colorspace.add_alpha(background, 1)

    masks = [(0.0, 1.0, 0.3, 0.2),
             (0.2, 0.6, 0.5, 0.45),
             (0.9, 0.4, 0.1, 0.4),
             (0.65, 0.85, 0.2, 0.15)]

    for x, y, w, h in masks:
        source_sub = transform.crop(source,x,y,w,h,relative=True)
        dest_sub = transform.crop(dest,x,y,w,h,relative=True)
        patch = transform.composite(source_sub, dest_sub,
                                    alpha_composite_function=alpha_composite,
                                    color_composite_function=color_composite)
        source = transform.substitute(source, patch, x, y, relative=True)

    image = transform.composite(source, background, 'add')
    image = transform.normalize(image)
    image = arrange.border(image, 200, 1)

    return image


# COMPILE PIECES | XXXX-XX-XX

pieces = [('taughannock_1', 'taughannock_2')]

os.makedirs('output', exist_ok=True)
for source, dest in pieces:
    A = dmtools.read(f"input/{source}.png")
    B = dmtools.read(f"input/{dest}.png")
    image = f(A, B)
    path = f"output/{source}_{dest}_composite.png"
    dmtools.write_png(image, path, versioning=True)
