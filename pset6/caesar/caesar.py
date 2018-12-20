import cs50
import sys

#command = sys.argv[1]

key = int(sys.argv[1])

text = cs50.get_string("Enter text: ")

#text.isalpha()
#text.isupper()
#text.islower()

#print(ord("a"))
#print(chr(97))
print("ciphertext: ", end="")

for i in text:
    #check if character is alphabetic
    if i.isalpha():
        #check if character is uppercase
        if i.isupper():
            #convert character to ASCII value and encipher using key
            upper = ((((ord(i) + key) - 65) % 26) + 65)
            #convert character back to alphabetical and print
            print(chr(upper), end="")
        #check if character is lowercase
        elif i.islower():
            #convert character to ASCII value and encipher using key
            lower = ((((ord(i) + key) - 97) % 26) + 97)
            #convert character back to alphabetical and print
            print(chr(lower), end="")
    #print non-alphabetical characters
    else:
        print(i, end="")
print()