/**
 * recover.c
 *
 * Computer Science 50
 * Problem Set 4
 *
 * Recovers JPEGs from a forensic image.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t  BYTE;

int main(int argc, char* argv[])
{
    BYTE buffer[512];
    char title[50];
    int fileNum = 0;

    //opening card.raw
    FILE* card = fopen("card.raw", "r");
    if (card == NULL)
    {
        fclose(card);
        printf("Could not create");
        return 2;
    }

    // temporary declaring img
    FILE* img = NULL;

    /* repeat untill end of file reached reached,
       read 512 bytes at a time from card */
    while ((fread(&buffer, sizeof(BYTE), 512, card)) != 0 )
    {
        //if it's a start of a jpg, open a new file and start writing to it.
        if (buffer[0] == 0xff && buffer[1] ==  0xd8 && buffer[2] ==  0xff && (buffer[3] == 0xe0 || buffer[3] == 0xe1))
        {
            sprintf(title, "%03d.jpg", fileNum);
            img = fopen(title, "w");
            if (img == NULL)
            {
                fclose(img);
                printf("Could not create");
                return 3;
            }
            fileNum++;

            fwrite(&buffer,  sizeof(BYTE), 512, img);
        }

        //else, continue writing to it.
        else if (fileNum != 0)
        {
            fwrite(&buffer,  sizeof(BYTE), 512, img);
        }
    }

    //close img
    fclose(img);
    //close card
    fclose(card);
}
