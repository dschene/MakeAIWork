import pickle

###########################################

#working directory is Project_1 map

model = pickle.load(open('./models/models_2.pkl', 'rb'))

#for v in model.items():
#    print(v)


model_variables = model['coefficients']
m_intercept = model['intercept']
ranges = model['ranges']

###########################################

def get_value(input_range, variable_name, criteria):
    counter = 3
    while counter > 0:
        try:
            patient_value_1 = float(input(f"Please enter {variable_name} in {criteria}. This number has to be between {input_range[0]} and {input_range[1]}: "))
        except ValueError:
            print(f'Invalid entry. You have {counter-1} attempts left.')
            counter -= 1
            continue
        if (input_range[0] <= patient_value_1 <= input_range[1]):
            return (patient_value_1)
            break
        else:
            print(f'Invalid entry. You have {counter-1} attempts left.')
            counter -= 1
            continue
    
    print('You have provided too many invalid inputs. The programme will now shut down automatically.')
    exit()

b_1, b_2 = m_intercept, m_intercept
first_values = {}

for v in model_variables.keys():
    if v == 'BMI':
        for x in ['mass', 'length']:
            if x == 'mass':
                p_mass = get_value(ranges[x], x, ranges[x][2])
                first_values['mass'] = p_mass
            else:  
                p_height = get_value(ranges[x], x, ranges[x][2])  
                first_values['height'] = p_height
        b_1 += (p_mass / (p_height * 100)**2) * model_variables['BMI']
    else:
        dummy_v = (get_value(ranges[v], v, ranges[v][2]))
        b_1  += (dummy_v * model_variables[v])
        first_values[v] = dummy_v

if b_1 < 0:
    print(f'Based on the provided data, this person will on average live {round(b_1)} years less because of their current lifestyle.')
elif b_1 > 0:
    print(f'Based on the provided data, this person will on average live {round(b_1)} years longer because of their current lifestyle.')

y_or_n = input("Would you like to provide another set of values? Enter 'y' for yes, 'n' for no.")

if y_or_n == 'y':
    print('You can now enter the second set of variables.')

    for v in model_variables.keys():
        if v == 'BMI':
            for x in ['mass', 'length']:
                if x == 'mass':
                    print(f'The previous value for {x} was {first_values[x]}')
                    p_mass_2 = get_value(ranges[x], x, ranges[x][2])
                else:  
                    p_height_2 = p_height  

            b_2 += (p_mass_2 / (p_height_2 * 100)**2) * model_variables['BMI']

        else:
            print(f'The previous value for {v} was {first_values[v]}')
            b_2 += (get_value(ranges[v], v, ranges[v][2])) * model_variables[v]

else:
    print('The programme will now shut down automatically')
    exit()

if b_1 < b_2:
    print(f'The lifestyle changes provided the second time will on average result in a lifespan increase of {round(b_2 - b_1)} years.')
else:
    print(f'The lifestyle changes provided the second time will on average result in a lifespan decrease of {round(b_1 - b_2)} years.')

