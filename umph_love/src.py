import os
import numpy as np
from scipy.io import wavfile
import dmtools
from dmtools import transform, arrange

colors = [(233, 18, 95),
          (27, 5, 246),
          (241, 187, 32),
          (0,0,0)]

images = []
songs = os.listdir("input/2012-09-22_louisville_ky")
songs.sort()
for song in songs:

    sample_rate, tmp = wavfile.read(f"input/2012-09-22_louisville_ky/{song}")

    l, _ = tmp.shape
    l = int(np.floor(l / sample_rate))

    tmp = tmp[:l*sample_rate,0].reshape((sample_rate, l))
    tmp = np.mean(tmp, axis=0)

    tmp = np.abs(tmp)
    tmp = (tmp - np.min(tmp)) / (np.max(tmp) - np.min(tmp))
    # tmp = (tmp + 2**15) / 2**16  # normalize

    n = 2**5
    m = 2**5

    image = np.array([colors[round(p*3)] for p in tmp[:n*m]]) / 255
    fill = np.zeros(((n*m - image.shape[0]), 3))
    image = np.vstack((image, fill))
    image = image.reshape((n,m,3))  # front
    # image = tmp[-(n*m+1):-1,0].reshape((n,m))  # back

    image = transform.rescale(image, 5)
    images.append(image)

image = arrange.image_grid(images, 7, 3, 50, 0)

dmtools.write_png(image, "output/all_in_time.png", versioning=True)



# def f(image:np.ndarray) -> np.ndarray:
#     return image


# # COMPILE PIECES | XXXX-XX-XX

# pieces = [('beebe_trail')]

# os.makedirs('output', exist_ok=True)
# for name in pieces:
#     image = dmtools.read('input/%s.ppm' % name)
#     image = f(image)
#     path = "output/%s_template" % name
#     dmtools.write_png(image, path)
