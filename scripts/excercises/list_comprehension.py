x = [1,2,3,4,5,6,7,8,9,10]

for i in x:
    if i % 2 == 0:
        print(i*2)
    else:
        print('number is not even')

# do_this if (condition) else do_that for item in list if item (condition)

emp_list = []

#voor list_item in list
for i in x:
    #ALS contidie #1
    if i > 5:
        #ALS conditie #2
        if i % 2 == 0:
            emp_list.append(i * 2)
        else:
            emp_list.append('not even')
    else:
        continue

print(emp_list)

print([i*2 if i%2 == 0 else 'not even' for i in x if i > 5])