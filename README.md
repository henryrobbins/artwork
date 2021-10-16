![banner](banner.png)
*water_cup_mod_7*

# Archive of Artwork

The complete archive of work can be compiled with

```
git clone git@github.com:henryrobbins/artwork.git
cd artwork
make all-works
```

Once compiled, an archive directory can be created with

```
make archive
```

Additionally, the `netpbm-works`, `animation-works`, and `ascii-works` targets
can be used to compile a subset of the work. Furthermore, individual series of
work can be compiled by navigating to the corresponding directory and running
the python script. The example below compiles the mod series.

```
cd netpbm/mod
python mod.py
```

| Title | Date | Work | Description |
|-------|------|------|-------------|
| spin | 2021-02-08 | [spin](spin) | [README.md](spin/README.md) |
| format | 2021-02-08 | [format](format) | [README.md](format/README.md) |
| mother_of_all_demos | 2021-02-24 | [mother_of_all_demos.pbm](netpbm/mother_of_all_demos/mother_of_all_demos.pbm) | [README.md](netpbm/mother_of_all_demos/README.md) |
| color_matrix | 2021-02-24 | [color_matrix.ppm](netpbm/color_matrix/color_matrix.ppm) | [README.md](netpbm/color_matrix/README.md) |
| polyominoes | 2021-02-26 | [polyominoes.pbm](netpbm/polyominoes/polyominoes.pbm) | [README.md](netpbm/polyominoes/README.md) |
| dissolve | 2021-03-02 | [dissolve](netpbm/dissolve) | [README.md](netpbm/dissolve/README.md) |
| mod | 2021-03-07 | [mod](netpbm/mod) | [README.md](netpbm/mod/README.md) |
| drunk_walk | 2021-03-17 | [drunk_walk](netpbm/drunk_walk) | [README.md](netpbm/drunk_walk/README.md) |
| partition | 2021-03-20 | [partition](netpbm/partition) | [README.md](netpbm/partition/README.md) |
| clip | 2021-03-23 | [clip](netpbm/clip) | [README.md](netpbm/clip/README.md) |
| channel | 2021-03-29 | [channel](netpbm/channel) | [README.md](netpbm/channel/README.md) |
| resolution | 2021-04-04 | [resolution](netpbm/resolution) | [README.md](netpbm/resolution/README.md) |
| stewart (WIP) | 2021-04-14 | [stewart](animation/stewart) | [README.md](animation/stewart/README.md) |
| conway | 2021-05-02 | [conway](netpbm/conway) | [README.md](netpbm/conway/README.md) |
| steal_your_face | 2021-05-12 | [steal_your_face](ascii/steal_your_face) | [README.md](ascii/steal_your_face/README.md) |
| weierstrass | WIP | [weierstrass](weierstrass) | [README.md](weierstrass/README.md) |

**NOTE:** Work dated between 2021-02-08 and 2021-05-12 was created for
[ART 3699](https://classes.cornell.edu/browse/roster/SP21/class/ART/3699), a
special topics photography class in which the topic was "Images and Algorithms".

## License

All artistic works in this project are licensed under the [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International](https://creativecommons.org/licenses/by-nc-nd/4.0/) license, and the underlying source code is licensed
under the [MIT license](LICENSE.md).
