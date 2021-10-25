import dmtools
from dmtools import ascii, colorspace
import logging
logging.basicConfig(filename='steal_your_face.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')

image = dmtools.read_netpbm("steal_your_face.ppm")
image = colorspace.RGB_to_gray(image)
ascii_img = ascii.image_to_ascii(image)
ascii_img.to_png("steal_your_face.png")

works = ['steal_your_face.png']
with open("works.txt", "w") as f:
    f.writelines(works)
