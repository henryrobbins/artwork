import os
import numpy as np
import dmtools


def f(img_1:np.ndarray, img_2:np.ndarray) -> np.ndarray:
    return dmtools.transform.wraparound(img_1 - 2*img_2)


# pieces = list(((i,j) for i in os.listdir("input") for j in os.listdir("input")))
pieces = [("new_haven.png", "tickets_1.png"),
          ("tickets_1", "pelham_4"),
          ("tickets_1", "stamford"),
          ("23_street", "23_street_glitch_1"),
          ("port_chester_train", "port_chester")]

os.makedirs('output', exist_ok=True)
for name_1, name_2 in pieces:
    if name_1 == ".DS_Store" or name_2 == ".DS_Store":
        continue
    name_1 = os.path.splitext(name_1)[0]
    name_2 = os.path.splitext(name_2)[0]

    img_1 = dmtools.read('input/%s.png' % name_1)
    img_1 = dmtools.colorspace.RGB_to_gray(img_1)

    img_2 = dmtools.read('input/%s.png' % name_2)
    img_2 = dmtools.colorspace.RGB_to_gray(img_2)

    image = f(img_1, img_2)
    path = f"output/{name_1}_{name_2}_weave.png"
    dmtools.write_png(image, path)

# file_name = "output/animation.mp4"
# dmtools.animation.to_mp4(frames=frames, path=file_name, fps=20, s=8)