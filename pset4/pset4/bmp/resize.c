/**
 * resize.c
 *
 * Computer Science 50
 * Problem Set 4
 *
 * Resizes a BMP.
 */

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char* argv[])
{
    int i, j, k, line, biHeight, m;
    // ensure proper usage
    if (argc != 4)
    {
        printf("Usage: ./resize n infile outfile\n");
        return 1;
    }

    // remember magnification factor
    int n = atoi(argv[1]);
    if (n < 1 || n > 100)
    {
        printf("n must be between 1 and 100");
        return 1;
    }

    // remember filenames
    char* infile = argv[2];
    char* outfile = argv[3];

    // open input file
    FILE* inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE* outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    
    // determine padding for scanlines
    int padding =  (4 - ((bi.biWidth) * sizeof(RGBTRIPLE)) % 4) % 4;
    
    // determine padding for outlines
    int paddingout =  (4 - (bi.biWidth * n * sizeof(RGBTRIPLE)) % 4) % 4;
    // fileheader changes
    bf.bfSize = (bi.biWidth * n * sizeof(RGBTRIPLE) + paddingout) * abs(n * bi.biHeight) + 54;
    
    // infoheader changes
    bi.biWidth *= n;
    bi.biHeight *= n;
    bi.biSizeImage = bf.bfSize - 54;

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    
    // iterate over infile's scanlines
    for (i = 0, biHeight = abs(bi.biHeight); i < (biHeight / n); i++)
    {
        for(line = 0;line < n;line++)
        {
            // iterate over pixels in scanline
            for (j = 0; j < (bi.biWidth / n); j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
        
                // write RGB triple to outfile
                for(m = 0;m < n;m++)
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            
            }
       

            // skip over padding, if any
            fseek(inptr, padding, SEEK_CUR);
    
            // then add it back (to demonstrate how)
            for (k = 0; k < paddingout; k++)
            {
                fputc(0x00, outptr);
            }
        
            if (line < n - 1)
                fseek(inptr, -((bi.biWidth / n) * sizeof(RGBTRIPLE) + padding),SEEK_CUR);
        }

    }
    
   

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // that's all folks
    return 0;
}
