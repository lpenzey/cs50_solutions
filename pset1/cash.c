#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float cash;

    do
    {
        cash = get_float("Enter amount of change to be counted: ");
    }
    while (cash <= 0);
    // round float and convert to int
    int cents;
    cents = roundf(cash * 100);


    // count the number of coins
    int counter;
    counter = 0;

    // find number of quarters
    while (cents >= 25)
    {
        counter += 1;
        cents = cents - 25;
    }

    // find number of dimes
    while (cents >= 10)
    {
        cents = cents - 10;
        counter += 1;
    }

    // find number of nickels
    while (cents >= 5)
    {
        cents = cents - 5;
        counter += 1;
    }

    // find number of pennies
    while (cents < 5 && cents > 0)
    {
        cents = cents - 1;
        counter += 1;
    }

    printf("%d\n", counter);

    return 0;
}