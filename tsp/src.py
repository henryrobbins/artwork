import os
import numpy as np
import dmtools
from dmtools import transform, arrange
from concorde.tsp import TSPSolver
np.random.seed(3093)


palette = [(234, 232, 255),
           (45, 49, 66),
           (176, 215, 255),
           (144, 174, 208),
           (111, 132, 161),
           (128, 153, 185),
           (120, 143, 173)]

def tsp(x,y,w,h):
    x = list(np.array(x))
    y = list(np.array(y))
    image = np.zeros((h,w,3))
    for i in range(h):
        for j in range(w):
            solver = TSPSolver.from_data((x+[j]), (y+[i]), norm='EUC_2D')
            sol = solver.solve()
            tour = list(sol.tour)
            if tour.index(1) > tour.index(2):
                tour.reverse()
            index = tour[tour.index(len(x)) - 1]
            color = np.array([palette[index]]) / 255
            image[i,j,:] = sol.optimal_value * color
    image = transform.normalize(image)
    return image


def tsp_grid(lb,ub,n,s,w,h,b):
    images = []
    for _ in range(w*h):
        x = np.random.uniform(lb,ub,n)
        y = np.random.uniform(lb,ub,n)
        images.append(tsp(x,y,s,s))
    image = arrange.image_grid(images,w,h,b)
    image = transform.rescale(image, 20, "point")
    return image


# COMPILE PIECES | 2021-10-31

pieces = [('hex',-1,7,6,6,6,6,1),
          ('pent',-1,7,6,5,6,6,1),
          ('tri',0,20,3,20,2,2,2)]

os.makedirs('output', exist_ok=True)
for name,lb,ub,n,s,w,h,b in pieces:
    image = tsp_grid(lb,ub,n,s,w,h,b)
    path = f"output/{name}_tsp.png"
    dmtools.write_png(image, path)
