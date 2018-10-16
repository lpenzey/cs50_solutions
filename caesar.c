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
        printf("Wrong number of arguments, try again!");
        return 1;
    }
    //converts the cipher key into an integer
    int k = atoi(argv[1]);
    //asks the user for a plaintext phrase to encode
    string start_text = get_string("Plaintext: ");
    //declares a variable equal to the length of the plaintext phrase above
    int n = strlen(start_text);

    printf("ciphertext: ");
    //loop through each character in the string
    for (int i = 0; n > i ; i++)
    {
        //checks if character is uppercase and then prints the rotated character using the key
        if (isupper(start_text[i]))
        {
            printf("%c", (((start_text[i] + k) - 65) % 26) + 65);
        }
        //checks if character is lowercase and then prints the rotated character using the key
        else if (islower(start_text[i]))
        {
            printf("%c", (((start_text[i] + k) - 97) % 26) + 97);
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