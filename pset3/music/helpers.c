// Helper functions for music

#include <cs50.h>
#include <math.h>
#include <string.h>
#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    //If numerator is one
    if (fraction[0] == '1')
    {
        //If denomenator is 8
        if (fraction[2] == '8')
        {
            return 1;
        }
        else if (fraction[2] == '4')
        {
            return 2;
        }
        else if (fraction[2] == '2')
        {
            return 4;
        }
        else if (fraction[2] == '1')
        {
            return 8;
        }
    }
    //checks for 3/8 time signature
    else if (fraction[0] == '3' && fraction[2] == '8')
    {
        return 3;
    }
    else
    {
        return 0;
    }
    return 0;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    int octave = note[strlen(note) - 1] - '0';

    // Base frequency of A4 is 440hz
    double freq = 440.0;

    // Adjust for letter
    switch (note[0])
    {
        case 'C':
            freq /= pow(2.0, 9.0 / 12.0);
            break;

        case 'D':
            freq /= pow(2.0, 7.0 / 12.0);
            break;

        case 'E':
            freq /= pow(2.0, 5.0 / 12.0);
            break;

        case 'F':
            freq /= pow(2.0, 4.0 / 12.0);
            break;

        case 'G':
            freq /= pow(2.0, 2.0 / 12.0);
            break;

        case 'A':
            break;
        case 'B':
            freq *= pow(2.0, 2.0 / 12.0);
            break;
    }
    //Octave Adjusment
    if (octave > 4)
    {
        freq *= pow(2.0, octave - 4);
    }
    else if (octave < 4)
    {
        freq /= pow(2.0, 4 - octave);
    }

    //Adjustment for accidentals
    if (note[1] == 'b')
    {
        freq /= pow(2.0, 1.0 / 12.0);
    }
    else if (note[1] == '#')
    {
        freq *= pow(2.0, 1.0 / 12.0);
    }

    return round(freq);
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    return strlen(s) == 0;
}