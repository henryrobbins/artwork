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
