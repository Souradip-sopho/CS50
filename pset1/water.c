#include <stdio.h>
#include <cs50.h>
int main(void)
{
    int min;
   
    do
    {
         printf("minutes: ");
        min=GetInt();
    }
    while(min<=0);
    printf("bottles: ");
    printf("%d\n",min*12);
    //return 0;
}