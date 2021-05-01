**Henry Robbins**<br/>
*format* (2021-02-08)<br/>
Python script

`format.py` is a Python script which takes two arguments: a text file and an
integer w. The text is optimally split into lines with a target line width of
w. This optimization is done via a reduction to the shortest path problem in
which Dijksta's algorithm finds an optimal s-t path. The script visualizes the
text changing as Dijkstra's algorithm continuously updates and finds the
optimal line break locations. Once the optimal solution is found, the
visualization loops. Pressing CTRL+C terminates the program. An example call is
given below.

```
# visualize the optimal splitting of short_text.txt to lines of length 45
python format.py short_text.txt 45
```
