**Henry Robbins and Ella Clemons**<br/>
*mod* (2021-03-07)<br/>
Netpbm (P2) and MPEG-4

The images sky (2021-02-24), faces (2021-03-07), and stomp (2021-03-07)
were photographed by Ella Clemons.

This work focuses on a particular image transformation technique: taking the
mod of an image. Here, "taking an image mod k" refers to taking the value of
every pixel mod k to create the transformed image. In addition to stills, this
work also includes an animation consiting of the image mod k for k in [1..150].

To compile this work, use the following commands.

```
# repo not yet cloned
git clone git@github.com:henryrobbins/art-3699.git
cd art-3699
python netpbm/mod/mod.py

# repo already cloned
python netpbm/mod/mod.py
```