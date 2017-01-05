#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
// #define FOR(i,n) for(i=0;i<n;i++)


int main(int argc, string argv[])
{
    int i, k, len;
    if (argc != 2)
    {   
        printf("Usage: ./caesar <key>\n");
        return 1;
    }
    else
        k = atoi(argv[1]);
    string ptext = GetString();
    len = strlen(ptext);
    for(i = 0;i < len;i++)
    {
        if (isalpha(ptext[i]) && isupper(ptext[i]))
            ptext[i] = (ptext[i] - 'A' + k) % 26 + 'A';
        if (isalpha(ptext[i]) && islower(ptext[i]))
            ptext[i] = (ptext[i] - 'a' + k) % 26 + 'a';
        printf("%c",ptext[i]);
    }
    printf("\n");
    return 0;
}

