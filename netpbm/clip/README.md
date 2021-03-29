## clip | 2021-03-23

This work was inspired by the partition series in which images were partitioned
by gradients in the image. This work continues with that idea and "clips" out
all but a select few gradients in the image. This technique exposes minimal
representations of the figures which lie in the selected range of gradients.

In some cases, unedited photos were taken by another photographer.
- creek: River Chavez (2021-03-21)

To compile this work, use the following commands.

```
# repo not yet cloned
git clone git@github.com:henryrobbins/art-3699.git
cd art-3699
python netpbm/clip/clip.py

# repo already cloned
python netpbm/clip/clip.py
```