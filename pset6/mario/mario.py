import cs50

#get input from user
height = cs50.get_int("Pyramid height:")

#validate input
while height < 0 or height > 23:
    if height > 0 and height < 23:
        break
    height = cs50.get_int("Pyramid height: ")

#for every row print spaces, print hashes, print a new line
for i in range(height):
    # print spaces
    for j in range(height - i -1):
        print(" ", end="")
    # print hashes
    for k in range(i + 2):
        print("#", end="")
    # print a new line
    print()