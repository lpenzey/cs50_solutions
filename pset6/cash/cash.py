import cs50

# get and validate input
while True:
    dollars = cs50.get_float("Enter amount of change to be counted: ")
    if dollars > 0:
        break

#convert dollars to cents and round
cents = round(dollars * 100)
coins = 0

while cents > 0:
    #count quarters
    if cents >= 25:
        cents -= 25
        coins += 1

    #count dimes
    elif cents >= 10:
        cents -= 10
        coins += 1

    #count nickels
    elif cents >= 5:
        cents -= 5
        coins += 1

    #add remaining pennies
    elif cents >= 1:
        cents -= 1
        coins += 1

#print result
print(coins)