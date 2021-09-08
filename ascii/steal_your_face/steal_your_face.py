from dmtools import netpbm, ascii, colorspace
import logging
logging.basicConfig(filename='steal_your_face.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')

image = netpbm.read_netpbm("steal_your_face.ppm")
M = colorspace.RGB_to_gray(image.M)
h,w = M.shape
image = netpbm.Netpbm(P=2, w=w, h=h, k=image.k, M=M)
ascii_img = ascii.netpbm_to_ascii(image)
ascii.write(ascii_img, "steal_your_face.png", 'png')

works = ['steal_your_face.png']
with open("works.txt", "w") as f:
    f.writelines(works)
