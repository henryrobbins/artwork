## partition | 2021-03-20

In bringing digital images to life, the image must be "partitioned" by color to
allow different inks to print independently. This image transformation
technique is based on this idea. Each column corresponds to a different
gradient in the image. The first two rows highlight pixels of the corresponding
gradient in white and black respectivley. The next two rows highlight the
pixels and background in the color of the corresponding gradient.

In some cases, unedited photos were taken by another photographer.
- sky: Ella Clemons (2021-02-24)
- waterfall: River Chavez (2021-03-20)

To compile this work, use the following commands.

```
# repo not yet cloned
git clone git@github.com:henryrobbins/art-3699.git
cd art-3699
python netpbm/partition/partition.py

# repo already cloned
python netpbm/partition/partition.py
```
