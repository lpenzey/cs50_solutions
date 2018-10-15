#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;

    // prompts user for valid input
    do
    {
        printf("Pyramid height: ");
        height = get_int();
    }
    while (height < 0 || height > 23);

    // create number lines
    for (int line = 0; line < height; line++)
    {
        // create number spaces
        for (int spaces = height - line; spaces > 1; spaces--)
        {
            printf(" ");
        }
        // create number hashes
        for (int hashes = 0; hashes < line + 2; hashes++)
        {
            printf("#");
        }
        printf("\n");
    }
}