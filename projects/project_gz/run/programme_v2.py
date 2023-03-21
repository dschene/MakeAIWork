import pickle
import logging

#Ophalen van het model uit het pickle bestand
model = pickle.load(open('../models/models_2.pkl', 'rb'))

#Opslaan van verschillende onderdelen van het model in variabelen

#de coefficienten
model_variables = model['coefficients']
#de 'b' / intercept van het model 
m_intercept = model['intercept']
#de ranges waarbinnen de waardes moeten vallen
ranges = model['ranges']

#Deze functie gebruiken we om een inputwaarde van de gebruiker te verkrijgen, afhankelijk van welke variabele dit is
def get_value(input_range, variable_name, criteria):
    #max. inputs is 3
    counter = 3
    while counter > 0:
        try:
            #Vragen om een waarde, waarbij de variabele, eenheid en range verschillen.
            patient_value_1 = float(input(f"Please enter {variable_name} in {criteria}. This number has to be between {input_range[0]} and {input_range[1]}: "))
        except ValueError:
            print(f'Invalid entry. You have {counter-1} attempts left.')
            counter -= 1
            continue
        #input moet binnen range vallen
        if (input_range[0] <= patient_value_1 <= input_range[1]):
            return (patient_value_1)
            break
        else:
            print(f'Invalid entry. You have {counter-1} attempts left.')
            counter -= 1
            continue
    
    print('You have provided too many invalid inputs. The programme will now shut down automatically.')
    exit()

#Aangezien we de mogelijkheid willen hebben om twee setjes input te vergelijken, slaan we deze op als b_1 en b_2
b_1, b_2 = m_intercept, m_intercept
first_values = {}

#Voor elke variabel die we moeten hebben van de gebruiker roepen we de functie op - BMI wordt apart berekend
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

#Wat er terug komt is het aantal jaren dat de huidige levensstijl iemand kost/brengt. Iemand kan alsnog langer of korter leven, maar wat we
#met deze berekening proberen te voorspellen is het aandeel (in jaren) dat levensstijl heeft in het totaalplaatje van iemands levensduur.

if b_1 < 0:
    print(f"The provided lifestyle metrics of this person negatively impact their lifespan by {abs(round(b_1))} years.")
elif b_1 > 0:
    print(f"The provided lifestyle metrics of this person positively impact their lifespan by {abs(round(b_1))} years.")

#Om arts/patient de mogelijkheid te geven om veranderingen in levensstijl te 'simuleren' kunnen ze hier een tweede set variabelen invoeren
#Hier komt uit wat voor invloed de eventuele veranderingen in levensstijl zullen hebben t.o.v. van de huidige situatie

y_or_n = input("Would you like to provide another set of values for comparison? Enter 'y' for yes, 'n' for no: ")

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
    print(f'The provided changes in lifestyle are estimated to positively impact this person\'s lifespan by {round(b_2 - b_1)} years compared to the previous lifestyle metrics.')
else:
    print(f'The provided changes in lifestyle are estimated to negatively impact this person\'s lifespan by {round(b_2 - b_1)} years compared to the previous lifestyle metrics.')