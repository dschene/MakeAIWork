import time

alarm_counter = eval(input("How many second would you like to sleep?"))

while alarm_counter > 0:
    print(alarm_counter)
    time.sleep(1)
    alarm_counter -= 1

print("WAKE UP!")
print('\a')