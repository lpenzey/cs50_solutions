#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{
    // rejects running the program with incorrect number of arguments
    if (argc != 2)
    {
        printf("Incorrect number of arguments, try again!");
        return 1;
    }
    // rejects running the program with non alphabetical chars
    else
    {
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (!isalpha(argv[1][i]))
            {
                printf("Only alphabetical characters are allowed, try again!");

                return 1;
            }
        }
    }


    string key = argv[1];
    //asks the user for a plaintext phrase to encode
    string start_text = get_string("Plaintext: ");
    //declares a variable equal to the length of the plaintext phrase
    int string_length = strlen(start_text);
    //declares a variable equal to the length of the key phrase
    int key_length = strlen(key);
    printf("ciphertext: ");
    //loop through each character in the string
    for (int i = 0, j = 0, n = strlen(start_text); i < n; i++)
    {
        // Get key for this letter
        int letterKey = tolower(key[j % key_length]) - 'a';
        //checks if character is uppercase and then prints the rotated character using the key
        if (isupper(start_text[i]))
        {
            printf("%c", (((start_text[i] + letterKey) - 65) % 26) + 65);
            //only increments j when used in the cipher
            j++;
        }
        //checks if character is lowercase and then prints the rotated character using the key
        else if (islower(start_text[i]))
        {
            printf("%c", (((start_text[i] + letterKey) - 97) % 26) + 97);
            //only increments j when used in the cipher
            j++;
        }

        else
            //prints characters that aren't letters as is
        {
            printf("%c", start_text[i]);
        }
    }
    printf("\n");
    return 0;
}
