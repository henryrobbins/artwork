import os
import numpy as np
import dmtools
from dmtools.transform import rescale, ResizeFilterName
from assistant.help import get_metadata

def memory() -> np.ndarray:
    os.system('./memory > tmp.txt')
    array = open('tmp.txt').read().split(',')[:-1]
    os.system('rm tmp.txt')
    image = np.array([int(i) for i in array])
    image = image.reshape((128,128))
    image = rescale(image, 5, filter=ResizeFilterName.POINT)
    return image

os.makedirs('output', exist_ok=True)
for i in range(10):
    image = memory()
    path = f"output/memory_{i}.png"
    dmtools.write_png(image, path, metadata=get_metadata())
