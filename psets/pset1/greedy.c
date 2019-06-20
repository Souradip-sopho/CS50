#include <stdio.h>
#include <cs50.h>
#include <math.h>
int main(void)
{
   float x;
    printf("O hai ");
    do
    {
        printf("How much change is owed?\n");
        x=GetFloat();
    }
    while(x<=0);
    x=x*100;
    int temp=(int)round(x);//printf("%d",temp);
    int count=0;
    count+=temp/25;
    temp=temp%25;
    count+=temp/10;
    temp=temp%10;
    count+=temp/5;
    temp=temp%5;
    count+=temp;
    printf("%d\n",count);
}
    