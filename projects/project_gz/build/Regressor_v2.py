import pandas as pd
import sqlite3
import math
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pickle

########################################################

#Data ophalen uit database, de op te halen data is dus de output van onze pipeline
dbName = "../rest_server/medisch_centrum_randstad/data/db.sqlite3"
tableName = "regression_table_2"

dbConnection = sqlite3.connect(dbName)

#We doen een query en maken hier een pandas dataframe van
df = pd.read_sql_query(f"SELECT * FROM {tableName}", dbConnection)

#We sluiten de connectie
dbConnection.close()


########################################################

#Hier kunnen we verschillende subsets van de data maken, om zo voor elke subset een model te trainen en de modellen onderling
#te kunnen vergelijken

#alle variabelen
v1 = ['exercise', 'smoking', 'alcohol', 'sugar', 'BMI']
#enkel de 3 variabelen met de hoogste correlatiewaardes (zie notebook)
v2 = ['exercise', 'smoking', 'BMI'] 
#enkel de 2 sterkst correlerende variabelen
v3 = ['smoking', 'exercise']

#De (coefficienten van de) modellen worden uiteindelijk als dictionaries opgeslagen. Hierin willen we ook meegeven welke grenzen er zijn
#gekozen, en met welke eenheden we werken per variabel

range_dict = {
    'genetic':(40, 120, 'years'),
    'length':(147, 220, 'centimeters'),
    'mass':(50,175, 'kilograms'),
    'exercise': (0,6, 'hours per day'),
    'smoking':(0,25, 'sigarettes per day'),
    'alcohol':(0,7, 'glasses per day'),
    'lifespan':(40,120, 'years'),
    'sugar':(0,15, 'cubes per day')
}

#Een lijst van de verschillende subsets om de modellen mee te trainen. Deze lijst kan worden aangepast en uitgebreid mochten we andere
#selecties van de data willen gebruiken om de modellen te trainen

version_list = [v1, v2, v3]

########################################################

#Hieronder trainen we voor elke subset van de data een model, en slaan we elk model op in een lijst

#Lijst om modellen in te stoppen
models = []

#Functie voor het trainen van een model plus het ophalen van een aantal evaluatie metrics
def train_model(dataframe, version):
    
    #Twee subsets - in x hebben we de onafhankelijke variabelen, in y onze afhankelijke variabel
    x = dataframe[version]
    y = dataframe.loc[:, 'age_diff']
    
    #Splitten van data in train/test sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 42)
    
    #We specificeren het model en 'fitten' het op onze trainingsdata
    model = LinearRegression()
    model.fit(x_train, y_train)
    
    #We laten het model voorspellingen doen adhv de testdata
    #Voor de verschillende 'evaluatie' metrics maken we variabelen
    predictions = model.predict(x_test)
    model_name = version[1]
    model_m_sqe = mean_squared_error(y_test, predictions)
    model_m_abse = mean_absolute_error(y_test, predictions)
    rmse = math.sqrt(model_m_sqe)
    r2 = r2_score(y_test, predictions)
    coefs = dict(list(zip(x.columns, model.coef_)))
    intercept = model.intercept_
    
    #Per model krijgen we dus een dictionary terug met alle relevante informatie. 
    return {
            'model name': model_name,
            'model variables': ', '.join(version),
            'mean squared error': model_m_sqe,
            'mean absolute error': model_m_abse,
            'r squared': r2,
            'root mean squared error': rmse,
            'coefficients': coefs,
            'intercept': intercept,
            'ranges': range_dict,
    }


#Voor elke versie van de data wordt een model getraind:
for v in version_list:
    models.append(train_model(df, v))

#Hele omslachtige manier om een versienaam aan elk model te geven
n = 1
for model in models:
    model['model name'] = n
    n += 1


#We kiezen het model met de hoogste r-squared waarde (mate waarin het model de spreiding van de data kan verklaren)
models_compared = [(m['model name'], m['r squared']) for m in models]
best_model = max(models_compared,key=lambda item:item[1])

#Het 'beste' model slaan we op 
for m in models:
    if m['model name'] == best_model[0]:
        final_model = m

#Het beste model exporteren we
with open('../models/models_2.pkl', 'wb') as f:
    pickle.dump(final_model, f)