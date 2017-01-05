#include <stdio.h>
#include <cs50.h>
int main(void)
{
    int n;
    
    do
    {
        printf("Height: ");
        n=GetInt();
    }
    while(n<0||n>23);
    for(int i=0;i<n;i++)
    {
        int j;
        for(j=n-1-i;j>0;j--)
        printf(" ");
        for(j=0;j<i+2;j++)
        printf("#");
        printf("\n");
    }
    return 0;
}    