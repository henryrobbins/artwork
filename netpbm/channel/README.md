**Henry Robbins**<br/>
*channel* (2021-03-29)<br/>
Netpbm (P3)

This work was generated using code adapted from Dan Torop. His script separates
pixels of a P3 Netpbm image into the three color channels allowing each color
channel to be modified independently. I further generalized this script by
allowing for an anonymous function to be passed for each channel. The current
pieces explore the application of the sin, ceiling, and triangle wave fucntions.

To compile this work, use the following commands.

```
# repo not yet cloned
git clone git@github.com:henryrobbins/art-3699.git
cd art-3699
python netpbm/channel/channel.py

# repo already cloned
python netpbm/channel/channel.py
```
