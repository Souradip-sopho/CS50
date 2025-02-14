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
    BYTE read[512];
    char name[10];
    int file_num = 0;
    
    FILE* file = fopen("card.raw", "r");
    if (file == NULL)
    {
    	fclose(file);
        printf("Could not open %s.\n", name);
        return 2;
    }
    
    FILE* output = NULL;
    
    while((fread(read,sizeof(BYTE),512,file)) != 0)
    {

        if ((read[0] == 0xff) && (read[1] == 0xd8) && (read[2] == 0xff) && ((read[3] == 0xe0 || read[3] == 0xe1 || read[3] == 0xe2 || read[3] == 0xe3 || read[3] == 0xe4 || read[3] == 0xe5 || read[3] == 0xe6 || read[3] == 0xe7 || read[3] == 0xe8 || read[3] == 0xe9 || read[3] == 0xea || read[3] == 0xeb || read[3] == 0xec || read[3] == 0xed || read[3] == 0xee || read[3] == 0xef)))
        {
            sprintf(name, "%03d.jpg", file_num);
            output = fopen(name, "w");
            if (output == NULL)
            {
                fclose(output);
                fprintf(stderr, "Could not create %s.\n", name);
                return 3;
            }
            
            file_num++;
            fwrite(read,sizeof(BYTE),512,output);
            
            while ((fread(read,sizeof(BYTE),512,file) != 0) && !((read[0] == 0xff) && (read[1] == 0xd8) && (read[2] == 0xff) && (read[3] == 0xe0 || read[3] == 0xe1 || read[3] == 0xe2 || read[3] == 0xe3 || read[3] == 0xe4 || read[3] == 0xe5 || read[3] == 0xe6 || read[3] == 0xe7 || read[3] == 0xe8 || read[3] == 0xe9 || read[3] == 0xea || read[3] == 0xeb || read[3] == 0xec || read[3] == 0xed || read[3] == 0xee || read[3] == 0xef)))
            {
                fwrite(read,sizeof(BYTE),512,output);
            }
            fclose(output);
            fseek(file, -512 * sizeof(BYTE),SEEK_CUR);
            
        }
        

    }

    fclose(file);
}
