/**
 * dictionary.c
 *
 * Computer Science 50
 * Problem Set 5
 *
 * Implements a dictionary's functionality.
 */
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

typedef struct node 
{
	char Word[46];
	struct node* next;
} node;

node* hashtable[5000] = {NULL};
unsigned int num_words = 0;


unsigned long hash(char *str)
{
    unsigned long hash = 0;
    for (int i = 0, n = strlen(str); i < n; i++)
        hash = (hash << 2) ^ str[i];
    return hash % 5000;
}

bool search(unsigned long hashval, node* h[], char str[])
{
	node* temp = h[hashval];
	while (temp != NULL)
	{
		if (strcmp(temp->Word,str) == 0)
		    return true;
		else
		    temp = temp->next;		
	}
	return false;
}
/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char* word)
{
    int i, k, l = strlen(word);
    char res_word[l + 1];
    for(i = 0;i < l;i++)
    {    	
    	res_word[i] = tolower(word[i]);	
    }
    res_word[l] = '\0';
    k = hash(res_word);
    if (search(k,hashtable,res_word))
        return true;	
    else
        return false;
}

/**
 * Loads dictionary into memory.  Returns true if successful else false.
 */
bool load(const char* dictionary)
{
    FILE* infile = fopen(dictionary,"r");
    if (infile == NULL)
    {
    	fclose(infile);
    	return false;
    }
    char w[47];	
    while(fgets(w, sizeof(w), infile))
    {
    	w[strlen(w) - 1] = '\0';
    	if (hashtable[hash(w)] != NULL)
    	{
    		node* new_node = (node* ) malloc(sizeof(node));
    		new_node->next = hashtable[hash(w)];
    		hashtable[hash(w)] = new_node;
    		strcpy(hashtable[hash(w)]->Word, w);
    		//free(new_node);
    	}
    	else
    	{
    		node *temp= (node* ) malloc(sizeof(node));
    		hashtable[hash(w)] =temp;
    		hashtable[hash(w)]->next = NULL;
    		strcpy(hashtable[hash(w)]->Word, w);
    	}
    	num_words++;
    }
    fclose(infile);
    return true;
    
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    if (num_words == 0)
        return 0;
    else
        return num_words;
}

/**
 * Unloads dictionary from memory.  Returns true if successful else false.
 */
bool unload(void)
{
	int i;
	for (i = 0; i < 5000; i++)
	{
    	// check the table for a node at that index
        node* cursor = hashtable[i];
    	if (cursor)
    	{
    		// create a temporary node to save the position of the next node
    		node* temp = cursor->next;

    		// free the current node
    		free(cursor);

    		// move the cursor to the next node
            cursor = temp;
            free(temp);
        }
    }
    
    return true;
       
}