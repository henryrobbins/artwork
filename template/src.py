import os
import numpy as np
import dmtools

def f(image:np.ndarray) -> np.ndarray:
    return image


# COMPILE PIECES | XXXX-XX-XX

pieces = [('beebe_trail')]

os.makedirs('output', exist_ok=True)
for name in pieces:
    image = dmtools.read('input/%s.ppm' % name)
    image = f(image)
    path = "output/%s_template" % name
    dmtools.write_png(image, path)
