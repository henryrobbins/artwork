import dmtools
from dmtools import colorspace
import logging
logging.basicConfig(filename='steal_your_face.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')

image = dmtools.read_netpbm("steal_your_face.ppm")
image = colorspace.RGB_to_gray(image)
dmtools.write_ascii(image, "steal_your_face.png")

works = ['steal_your_face.png']
with open("works.txt", "w") as f:
    f.writelines(works)
