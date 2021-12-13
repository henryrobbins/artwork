import os
import dmtools
from dmtools import colorspace
import logging
logging.basicConfig(filename='steal_your_face.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')

image = dmtools.read_netpbm("input/steal_your_face.ppm")
image = colorspace.RGB_to_gray(image)
os.makedirs('output', exist_ok=True)
dmtools.write_ascii(image, "output/steal_your_face.png")
