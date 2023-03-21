import pickle

###########################################

model = pickle.load(open('../models/models.pkl', 'rb'))

model_variables = model['coefficients']
lifespan = model['intercept']
ranges = model['ranges']

###########################################

patient_lifespan = lifespan

def get_value(input_range, variable_name, criteria):
    counter = 3
    while counter > 0:
        try:
            patient_value = float(input(f"Please enter {variable_name} in {criteria}. This number has to be between {input_range[0]} and {input_range[1]}: "))
        except ValueError:
            print(f'Invalid entry. You have {counter-1} attempts left.')
            counter -= 1
            continue
        if input_range[0] <= patient_value <= input_range[1]:
            return patient_value
            break
        else:
            print(f'Invalid entry. You have {counter-1} attempts left.')
            counter -= 1
            continue
    
    print('You have provided too many invalid inputs. The programme will now shut down automatically.')
    exit()

for v in model_variables.keys():
    if v == 'BMI':
        for x in ['mass', 'length']:
            if x == 'mass':
                p_mass = get_value(ranges[x], x, ranges[x][2])
            else:  
                p_height = get_value(ranges[x], x, ranges[x][2])  
        lifespan += (p_mass / (p_height * 100)**2) * model_variables['BMI']
    else:
        lifespan += (get_value(ranges[v], v, ranges[v][2])) * model_variables[v]


print(f"Estimated lifespan of patient is {round(lifespan, 2)}")