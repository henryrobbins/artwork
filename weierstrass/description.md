In image rescaling, filters are carefully chosen to result in "good" rescaled
representations of an image. This work explores what happens when you lift that
constraint. An approximation of the
[Weierstrass](https://en.wikipedia.org/wiki/Weierstrass_function) function was
used as a weighting function for a custom filter with a large support. The
properties of the Weierstrass function result in the near total obfuscation of
the source image. The exceedingly complex and seemingly random results are, in
fact, completely deterministic.