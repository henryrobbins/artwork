The Travelling Salesman Problem
([TSP](https://en.wikipedia.org/wiki/Travelling_salesman_problem)) is an
example of a problem which is deceivingly challenging to solve. This work
utilizes that complexity for imagemaking. A set of *n* points are randomly
placed on a plane and the optimal tour is found. The optimal tour is then
recomputed for each pixel where that pixel is included as a point. The color
and brightness of the pixel correspond to the pixel's location in the tour and
the tour cost respectively.