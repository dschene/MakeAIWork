file_1 = open('test.txt', 'w')

for i in range(10):
    file_1.write("Hello, this is a file \n")

for l in range(10):
    file_1.write("This is another line \n")

file_1.close()

for l in open('test.txt'):
    print(l)