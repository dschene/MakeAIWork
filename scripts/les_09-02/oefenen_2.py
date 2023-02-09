#Ask user for an input string
i_string = input("Enter a string please: ")

#make counter variable
counter = 0
#for every letter in the input string

for l in i_string:

    #check if the current letter 
    if l in "aeoui":
        #update counter variable
        counter += 1

#print out the amount of vowels in the input string
print(f"This string has {counter} vowels")