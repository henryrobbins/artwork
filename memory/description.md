A [programming language specification](https://en.wikipedia.org/wiki/Programming_language_specification) describes the syntax and semantics of a
programming language. In some instances, the values of a term may be unspecified.
In [C](https://en.wikipedia.org/wiki/C_(programming_language)), the value of an
[uninitialized variable](https://en.wikipedia.org/wiki/Uninitialized_variable)
is unspecified. In some cases, the value will be the "contents of [the] memory...
[occupying] those addresses." The C program below was used to generate 32,768
uninitialized bytes. The program was compiled with Apple clang 12.0.5 on a
MacBookPro (15-inch, 2018) running macOS 11.4.0.

```c
#include <stdio.h>

#define N 32768

int main()
{
    int i;
    unsigned char arr[N];

    for (i = 0; i < N; ++i)
        printf("%d,", arr[i]);

    return 0;
}
```

These uninitialized bytes were then interpreted as grayscale image data and
layed atop other images.
