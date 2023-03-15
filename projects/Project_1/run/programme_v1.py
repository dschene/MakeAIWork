import pickle
import os, sys

###########################################

#os.chdir(os.path.dirname(sys.argv[0]))

model = pickle.load(open('../models/models.pkl', 'rb'))

model_variables = model['coefficients']

lifespan = model['intercept']

###########################################


for v in model_variables.items():

    if v[0] == 'genetic':

        lifespan += int(input('Genetic: ')) * v[1]

    if v[0] == 'exercise':

        lifespan += int(input('Exercise: ')) * v[1]

    if v[0] == 'smoking':

        lifespan += int(input('Smoking: ')) * v[1]
    
    if v[0] == 'alcohol':

        lifespan += int(input('Alcohol: ')) * v[1]

    if v[0] == 'sugar':
        
        lifespan += int(input('Sugar: ')) * v[1]

    if v[0] == 'BMI':

        weight = int(input('Mass: '))
        length = int(input('Length: '))
        bmi = weight / (length * 100)**2

        lifespan += (bmi * v[1])

print('\n')

print(f"Estimated lifespan is {round(lifespan, 2)}")