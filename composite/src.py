import os
import numpy as np
import dmtools
from dmtools import transform, colorspace
from dmtools.transform import CompositeOp, CompositeOpName
from typing import Callable


def safe_divide(n: np.ndarray, d: np.ndarray) -> np.ndarray:
    return np.divide(n, d, out=np.zeros_like(n), where=(d != 0))


def alpha_composite_1(aA, aB) -> np.ndarray:
    return np.sin(aA) * np.sin(aB)


def alpha_composite_2(aA, aB) -> np.ndarray:
    return np.abs(np.sin(aA)) * np.abs(np.sin(aB))


def alpha_composite_3(aA, aB) -> np.ndarray:
    return np.clip(aA + aB, 0, 1)


def color_composite_1(xA, aA, xB, aB, xaA, xaB, aR) -> np.ndarray:
    return safe_divide(xaA - xaB, aR)


def color_composite_2(xA, aA, xB, aB, xaA, xaB, aR) -> np.ndarray:
    return safe_divide(xaA * transform.clip(xaB*5), aR)


def f(source:np.ndarray, dest:np.ndarray, alpha_composite: Callable,
    color_composite: Callable, background_color: int, post: Callable) -> np.ndarray:
    # change alpha to 0.5 for both images
    source[:,:,3] = 0.5*source[:,:,3]
    dest[:,:,3] = 0.5*dest[:,:,3]

    # create a gray background
    n,m,*_ = source.shape
    background = np.ones((n,m,3)) * (background_color / 255)
    background = colorspace.add_alpha(background, 1)

    # composite the two images and the composite on background
    compsite_op = CompositeOp(alpha_composite, color_composite)
    image = transform.composite(source, dest, operator=compsite_op)
    image = transform.composite(image, background, CompositeOpName.ADD)

    # post-processing (if any)
    if post is not None:
        image = post(image)

    return image


pieces = [
    ('road_2', 'road_sunset', alpha_composite_1, color_composite_1, 40, transform.clip),
    ('road_2', 'road_sunset', alpha_composite_1, color_composite_1, 40, None),
    ('peeling', 'erosion', alpha_composite_2, color_composite_1, 70, transform.clip),
    ('erosion', 'peeling', alpha_composite_2, color_composite_1, 70, transform.clip),
    ('road_sunset', 'taughannock_1', alpha_composite_2, color_composite_1, 70, transform.clip),
    ('taughannock_1', 'road_sunset', alpha_composite_3, color_composite_2, 150, transform.normalize),
    ('taughannock_1', 'peeling', alpha_composite_2, color_composite_1, 70, transform.clip)
]

os.makedirs('output', exist_ok=True)
for source, dest, alpha, color, bg, post in pieces:
    A = dmtools.read(f"input/{source}.png")
    B = dmtools.read(f"input/{dest}.png")
    image = f(A, B, alpha, color, bg, post)
    if post is None:
        path = f"output/{source}_{dest}_composite.png"
    else:
        path = f"output/{source}_{dest}_{post.__name__}_composite.png"
    dmtools.write_png(image, path)
