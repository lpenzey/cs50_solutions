// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "dictionary.h"

// define node struct
typedef struct node
{
    char word[LENGTH + 1];
    struct node* next;
}
node;

// define array of node structs
node *hashtable[HASHTABLE_SIZE] = {NULL};

//initialize variable for word count
int word_count = 0;

//initialize variable for load state
bool loaded = false;

//define hash function (help from reddit user delipity: https://www.reddit.com/r/cs50/comments/1x6vc8/pset6_trie_vs_hashtable/cf9nlkn)
int hasher(char* word)
{
    unsigned int hash = 0;
    for (int i=0, n=strlen(word); i<n; i++)
        hash = (hash << 2) ^ word[i];
    return hash % HASHTABLE_SIZE;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initializes all array elements to be NULL
    for (int i = 0; i < HASHTABLE_SIZE; i++)
        {
            hashtable[i] = NULL;
        }
    //open dictionary file
    FILE *file = fopen(dictionary, "r");
    //check to see if dictionary actually loaded
    if (file == NULL)
    {
        return false;
    }

    //scan through dictionary until end of file
    while (true)
    {
        //allocate memory for each node
        node *new_node = malloc(sizeof(node));
        //check for successful memory allocation
        if (new_node == NULL)
        {
            fprintf(stderr, "Not enough memory :(\n");
            return false;
        }

        //read word from file and in new_word
        fscanf(file, "%s", new_node->word);
        new_node->next = NULL;

        if (feof(file))
        {
            free(new_node);
            break;
        }

        //increment word count
        word_count ++;

        //hash the word
        int hashed_word = hasher(new_node->word);
        node *head = hashtable[hashed_word];

        //if index is empty insert first node
        if (head == NULL)
        {
            hashtable[hashed_word] = new_node;
        }

        //if index has elements put word in hashtable
        else
        {
            new_node->next = hashtable[hashed_word];
            hashtable[hashed_word] = new_node;
        }
    }
    //close dictionary file
    fclose(file);
    loaded = true;
    return true;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    //create space for copy of word adding one to account for string termination
    int word_length = strlen(word);
    char copy[word_length + 1];

    //convert to lowercase and store in copy
    for (int i = 0; i < word_length; i++)
    {
        copy[i] = tolower(word[i]);
    }

    //add string termination character (null pointer)
    copy[word_length] = '\0';

    //create hash value using hash function
    int hashed_word = hasher(copy);

    //assign pointer to first node
    node* pointer = hashtable[hashed_word];

    //run through to end of linked list
    while (pointer != NULL)
    {
        if (strcmp(pointer->word, copy) == 0)
        {
            //word has been found
            return true;
        }
        else
        {
            //word hasn't been found, check next node
            pointer = pointer->next;
        }
    }
    return false;
}



// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (loaded)
    {
        return word_count;
    }
    else
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < HASHTABLE_SIZE; i++)
    {
        node* pointer = hashtable[i];
        while (pointer != NULL)
        {
            node* temp = pointer;
            pointer = pointer->next;
            free(temp);
        }
    }
    loaded = false;
    return true;
}

