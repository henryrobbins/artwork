import os
import numpy as np
from numpy import random
import dmtools

def f(img_1:np.ndarray, img_2:np.ndarray) -> np.ndarray:

    # h,w = (np.array(img_1.shape)/7).astype(int)

    # a = np.empty((int(h * 0.5), w))
    # a[:,::2] = 0
    # a[:,1::2] = 1

    # b = np.empty((int(h * (1 - 0.5)), w))
    # b[:,::2] = 1
    # b[:,1::2] = 0

    # A = np.vstack((a,b))
    # np.random.shuffle(A)

    A = random.randint(0, 2, img_1.shape)
    # A = random.randint(0, 2, (np.array(img_1.shape)/4).astype(int))
    # A = dmtools.transform.rescale(A,7)
    image = (A * img_1) + (~A * img_2)
    # image = (A * img_1) + ((-A + 1) * img_2)
    return dmtools.transform.normalize(image)
    # return image


# pieces = ((i,j) for i in os.listdir("input") for j in os.listdir("input"))
pieces = [("new_haven.png", "tickets_1.png")]

os.makedirs('output', exist_ok=True)
for name_1, name_2 in pieces:
    if name_1 == ".DS_Store" or name_2 == ".DS_Store":
        continue
    name_1 = os.path.splitext(name_1)[0]
    name_2 = os.path.splitext(name_2)[0]

    img_1 = dmtools.read('input/%s.png' % name_1)
    img_1 = dmtools.transform.rescale(img_1, 0.25, filter="triangle")
    img_1 = dmtools.colorspace.RGB_to_gray(img_1)

    img_2 = dmtools.read('input/%s.png' % name_2)
    img_2 = dmtools.transform.rescale(img_2, 0.25, filter="triangle")
    img_2 = dmtools.colorspace.RGB_to_gray(img_2)

    image = f(img_1, img_2)
    path = f"output/{name_1}_{name_2}_weave.png"
    dmtools.write_png(image, path, versioning=True)
