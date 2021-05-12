**Henry Robbins**<br/>
*dissolve* (2021-03-02)<br/>
Netpbm (P2)

This series contains two groups of images: those that were hand-crafted and
those that were created by a script. dissolve.pgm, dissolve2.pgm, and
dissolve3.pgm were hand-crafted (2021-02-26). The beebe_trail subseries is
generated via a script (2021-03-02). Both are based on the same principle:
dissolving a vector of pixels. A plan was chosen to iteratively update a vector
of pixels converging to a vector of black pixels. This plan was inspired by the
rule for toppling [sandpiles](https://www.youtube.com/watch?v=1MtEUErz7Gg).

The three hand-crafted images begin with different lengths of a random vector.
The columns from the left to the right of the image show how the vector is
updated until it dissolves completely.

For the beebe_trail subseries, this same plan was implemented programatically.
A vector (some row in the case of 'h' and column in the case of 'w') at
location i is chosen from the image to dissolve. In some images, consecutive
dissolves are applied. For example, beebe_trail_h60v47 is acheived by first
dissolving down from row 60 and then dissolving to the left from column 47.

To compile this work, use the following commands.

```
# repo not yet cloned
git clone git@github.com:henryrobbins/art-3699.git
cd art-3699
python netpbm/dissolve/dissolve.py

# repo already cloned
python netpbm/dissolve/dissolve.py
```