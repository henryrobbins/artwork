import dmtools
from dmtools import transform, arrange, colorspace
import numpy as np
from concorde.tsp import TSPSolver
import logging
logging.basicConfig(filename='template.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')


def template(image:np.ndarray) -> np.ndarray:
    """TODO: Add description

    Args:
        image (netpbm.Netpbm): Netpbm image.

    Returns:
        netpbm.Netpbm: TODO: Add description
    """
    # TODO: Implement an interesting transformation!
    return image

np.random.seed(3093)


def tsp(s,x,y,w,h,has_color,c):
    """TODO"""
    w, h = w*s, h*s
    x = list(np.array(x) * s)
    y = list(np.array(y) * s)
    image = np.zeros((h,w,3))
    for i in range(h):
        for j in range(w):
            solver = TSPSolver.from_data((x+[j]),(y+[i]),norm='EUC_2D')
            sol = solver.solve()
            tour = list(sol.tour)
            if tour.index(1) > tour.index(2):
                tour.reverse()
            c_index = tour[tour.index(len(x)) - 1]
            if has_color:
                image[i,j,:] = sol.optimal_value * c[c_index]
            else:
                image[i,j,:] = sol.optimal_value * np.array([1,1,1])
    image = transform.normalize(image)
    return image


# COMPILE PIECES | XXXX-XX-XX

pieces = [('box',5,[5,5,10,10],[5,10,5,10],15,15,True,np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1]]))]
        #   ('h',3,[5,5,10,10,20,20,25,25,20,20,10,10],[5,35,35,23,23,35,35,5,5,17,17,5],30,40,False,None)]

# pieces = [('penta',3,47,5,50,3,3)]

works = []
for name,s,x,y,w,h,has_color,c in pieces:

# works = []
# for name,lb,ub,n,s,w,h in pieces:

    # images = []
    # for i in range(w*h):
    #     x = np.random.uniform(lb,ub,n)
    #     y = np.random.uniform(lb,ub,n)
    #     images.append(colorspace.RGB_to_gray(tsp(1,x,y,s,s,False,None)))

    # image = arrange.image_grid(images,w,h,1)

    image = tsp(s,x,y,w,h,has_color,c)
    image = transform.rescale(image, 10, "point")
    path = "%s_tsp.png" % name
    dmtools.write_png(image, path)
    works.append(path)

# TODO: uncomment this
# with open("works.txt", "w") as f:
#     for work in works:
#         f.write("%s\n" % work)
