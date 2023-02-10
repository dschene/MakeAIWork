#eerst willen we het volgende patroon:

#*
#**
#***
#****
#*****

#we maken een variabel aan en vragen de gebruiker om de hoogte
inp_height_1 = int(input("Geef een hoogte aan: "))

for i in range(1, inp_height_1 + 1):
    print('*' * i)

#nu willen we het patroon, maar dan omgekeerd

#*****
#****
#***
#**
#*

inp_height_2 = int(input("Geef een hoogte aan: "))

#voor het aantal rijen
for i in range(inp_height_2):
    #print het aantal sterren
    print(inp_height_2 * '*')
    #trek voor elke rij 1 ster af van het maximum
    inp_height_2 -= 1

#nu willen we het patroon, maar dan gespiegeld
#    *  - 4 spaties, 1 ster
#   **  - 3 spaties, 2 sterren
#  ***  - 2 spaties, 3 sterren
# ****  - 1 spaties, 4 sterren
#*****  - 0 spaties, 5 sterren

#voor elke rij willen we:
    #eerst een aantal spaties, namelijk de max hoogte - 1, en dan een ster *

inp_height_3 = int(input("Geef een hoogte aan: "))

#elke rij willen we eerst (max - 1) spaties, gevolgd door een ster
for i in range(1, inp_height_3 + 1):
    print(' ' * (inp_height_3 - 1) + ('*' * i))
    inp_height_3 -= 1

#nu willen we de andere variant gespiegeld:
#*****
# ****
#  ***
#   **
#    *


#elke rij willen we het (height) keer sterretjes, en (rij) keer spaties

inp_height_4 = int(input("Geef een hoogte aan: "))

for i in range(inp_height_4):
    print(('*' * inp_height_4) + (i * ' '))
    inp_height_4 -= 1

#nu willen we het volgende patroon:

#   *
#  ***
# *****
#*******
# *****
#  ***
#   *

#hier is de hoogte 4 en de breedte ook

inp_height_5 = int(input("Geef een hoogte aan: "))

#elke rij willen we:
#(aantal rijen - 1) spaties gevolgd door 1 ster


