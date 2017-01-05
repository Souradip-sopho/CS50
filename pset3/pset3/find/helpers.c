/**
 * helpers.c
 *
 * Computer Science 50
 * Problem Set 3
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    if (n <= 0)
        return false;
    else
    {
        int low = 0, high = n - 1;
        while(low <= high)
        {
            int mid = (low + high) / 2;
            if (values[mid] == value)
                return true;
            else
            {
                if (values[mid] > value)
                    high = mid - 1;
                else
                    low = mid + 1;
            }
        }
    }
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    if (n > 0)
    {
        int max = values[n - 1];
        int max_index = n - 1;
        for(int i = 0;i < n;i++)
        {
            if (values[i] > max)
            {
                max = values[i];
                max_index = i;
            }
        }
        int temp = values[n - 1];
        values[n - 1] = max;
        values[max_index] = temp;
        sort(values,n - 1);
        return;
    }
}
