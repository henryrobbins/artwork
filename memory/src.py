import os
import numpy as np
import dmtools
from dmtools import transform, colorspace
from assistant.help import get_metadata

def memory(base, n, m, inv_base, inv_mem, white_bg) -> np.ndarray:
    # get undefined numbers from C program
    os.system('./memory > tmp.txt')
    array = open('tmp.txt').read().split(',')[:-1]
    os.system('rm tmp.txt')
    array = array[-(n*m):]
    mem = np.array([int(i) for i in array])
    mem = mem.reshape((n,m)) / 256

    # layer randomness
    h,w = base.shape
    mem = transform.rescale(mem, w=w, h=h)
    f_base = (lambda x: -x + 1) if inv_base else (lambda x: x)
    f_mem = (lambda x: -x + 1) if inv_mem else (lambda x: x)
    tmp = transform.normalize(f_base(base) * f_mem(mem))
    if white_bg:
        image = np.where(mem == 0, 1, tmp)
    else:
        image = tmp

    return image

os.makedirs('output', exist_ok=True)

pieces = [("fence_glitched", 114, 152, True, True, False),
          ("fence_glitched", 114, 152, True, False, True),
          ("fence_house", 114, 152, True, True, False),
          ("lost_cat", 114, 152, True, True, False),
          ("lost_cat", 114, 152, True, False, False),
          ("lost_cat", 114, 152, True, False, True),
          ("street_light_1", 160, 120, False, True, False),
          ("street_light_1", 160, 120, True, False, False),
          ("street_light_2", 160, 120, True, True, False)]

for name, n, m, inv_base, inv_mem, white_bg in pieces:
    base = dmtools.read(f"input/{name}.png")
    base = colorspace.RGB_to_gray(base)
    # base = transform.rescale(base, k=0.25)
    image = memory(base, n, m, inv_base, inv_mem, white_bg)
    path = f"output/{name}_memory_{int(inv_base)}{int(inv_mem)}{int(white_bg)}.png"
    dmtools.write_png(image, path, metadata=get_metadata())
