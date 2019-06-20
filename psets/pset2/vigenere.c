#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
// #define FOR(i,n) for(i=0;i<n;i++)


int main(int argc, string argv[])
{
    int i, j, l;
    char* key;
    
    if (argc != 2)
    {
        printf("Usage: ./vigenere <keyword>\n");
        return 1;
    }
    else
    {
        int m;
        l = strlen(argv[1]);
        key = (char *) malloc((l + 1) * sizeof(char));
        for(m = 0;m < l;m++)
            key[m] = argv[1][m];
        key[l] = '\0';
    }
    for(i = 0;i < l;i++)
    {
        if (!isalpha(key[i]))
        {
    	    printf("Usage: ./vigenere <keyword>\n");
    	    return 1;
    	}
    	else
    	{
    	    if (isupper(key[i]))
    	        key[i] -= 'A';
    	    else
    	        key[i] -= 'a';
    	}
    }
    string ptext = GetString();
    j = 0 ;
    for(i = 0;i < strlen(ptext);i++)
    {
       
        if (isalpha(ptext[i]) && isupper(ptext[i]))
        {
            ptext[i] = (ptext[i] - 'A' + key[j]) % 26 + 'A';
            j = (j + 1) % l;
        }
        else if (isalpha(ptext[i]) && islower(ptext[i]))
        {
            ptext[i] = (ptext[i] - 'a' + key[j]) % 26 + 'a';
            j = (j + 1) % l;
        }
        printf("%c",ptext[i]);
    }
    printf("\n");
    free(key);
    return 0;
}

