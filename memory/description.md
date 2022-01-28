A [programming language specification](https://en.wikipedia.org/wiki/Programming_language_specification) describes the syntax and semantics of a
programming language. In some instances, the values of a term may be unspecified.
In [C](https://en.wikipedia.org/wiki/C_(programming_language)), the value of an
[uninitialized variable](https://en.wikipedia.org/wiki/Uninitialized_variable)
is unspecified. In some cases, the value will be the "contents of [the] memory...
[occupying] those addresses." A C program was used to generate 32,768
uninitialized bytes. The program was compiled with Apple clang 12.0.5 on a
MacBookPro (2018) running macOS 11.4.0. These uninitialized bytes were
then interpreted as grayscale image data and layed atop other images.
