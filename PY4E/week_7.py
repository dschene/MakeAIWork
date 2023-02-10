#creating file handle
fhandle = open('mbox.txt')

for l in fhandle:
    if '@uct.ac.za' not in l:
        continue
    print(l.rstrip())
