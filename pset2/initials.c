#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
// #define FOR(i,n) for(i=0;i<n;i++)

int main(void)
{
    int i;
    string name = GetString();
    printf("%c",toupper(name[0]));
    for(i = 0;i < strlen(name);i++)
    {
        if (isspace(name[i]))
        {
            printf("%c",toupper(name[i + 1]));
        }
    }
    printf("\n");
    return 0;
}