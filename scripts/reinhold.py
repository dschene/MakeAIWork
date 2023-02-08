from random import randint

print("*******************")
print("*******************")
print("*******************")
print("*******************")
print()
print("*******************")
print("*                 *")
print("*                 *")
print("*******************")
print()
print("*")
print("**")
print("***")
print("****")
print()

x = eval(input("Enter a number:"))


print(x, x*2, x*3, x*4, x*5, sep="---")

x_1 = randint(1,50)
x_2 = randint(2,5)
print(x_1**x_2)


string_1 = input("Enter a string: ")

print(len(string_1))
print(string_1*10)
print(string_1[0])
print(string_1[:2])
print(string_1[-3:])
print("".join(reversed(string_1)))

if len(string_1) >= 7:
    print(string_1[6])
else:
    print("not equal to or longer than 7")

print(string_1[1:-1])

print(string_1.upper())
print(string_1.replace('a', 'e'))
print()

for i in range(0, len(string_1)):

    if string_1[i].isalpha():
        print(string_1[i])
        string_1 = string_1.replace(string_1[i], " ")

        print(string_1)

string_2 = input("Enter another string: ")
print("Number of estimated words: ", string_2.count(" ") + 1)

f_1 = input("Enter a formula: ")
if f_1.count("(") == f_1.count(")"):
    print("Equal number of parentheses")

else:
    print("Unequal number of parentheses")
