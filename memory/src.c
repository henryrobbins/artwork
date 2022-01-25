#include <stdio.h>

#define N 128
#define M 128

unsigned char garbage();

int main()
{
    int i;
    unsigned char arr[N*M];

    for (i = 0; i < N*M; ++i)
        printf("%d,", arr[i]);   // garbage from uninitialized variable
        // printf("%d,", garbage());   // garbage from function with no return value

    return 0;
}

unsigned char garbage() {}
