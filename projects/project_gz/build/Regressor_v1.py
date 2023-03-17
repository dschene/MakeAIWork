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
tableName = "regression_table"

dbConnection = sqlite3.connect(dbName)

#We doen een query en maken hier een pandas dataframe van
df = pd.read_sql_query(f"SELECT * FROM {tableName}", dbConnection)

#We sluiten de connectie
dbConnection.close()

#Selecteren van relevante columns 
df_updated = df[['genetic', 'exercise', 'smoking', 'alcohol', 'sugar', 'BMI', 'lifespan']]

########################################################

#Hier kunnen we verschillende subsets van de data maken, om zo voor elke subset een model te trainen en onderling
#te vergelijken

v1 = ['genetic', 'exercise', 'smoking', 'alcohol', 'sugar', 'BMI']
v2 = ['genetic', 'exercise', 'smoking', 'BMI'] 
v3 = ['genetic', 'smoking']
v4 = ['genetic', 'exercise', 'smoking']
v5 = ['genetic', 'exercise', 'smoking', 'alcohol', 'sugar']

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

version_list = [v1, v2, v3, v4, v5]

########################################################

#Hier trainen we voor elke subset een model, en slaan we elk model op in een lijst

#Lijst om modellen in te stoppen
models = []

#Functie voor het trainen van een model plus het ophalen van een aantal evaluatie metrics
def train_model(dataframe, version):
    
    x = dataframe[version]
    y = dataframe.loc[:, 'lifespan']
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 42)
    
    model = LinearRegression()
    model.fit(x_train, y_train)
    
    predictions = model.predict(x_test)
    
    model_name = version[1]
    model_m_sqe = mean_squared_error(y_test, predictions)
    model_m_abse = mean_absolute_error(y_test, predictions)
    rmse = math.sqrt(model_m_sqe)
    r2 = r2_score(y_test, predictions)
    coefs = dict(list(zip(x.columns, model.coef_)))
    intercept = model.intercept_
    
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



#Voor elke versie van de data een model trainen:
for v in version_list:
    models.append(train_model(df_updated, v))

#Hele omslachtige manier om een versienaam aan elk model te geven
n = 1
for model in models:
    model['model name'] = n
    n += 1

########################################################

models_compared = [(m['model name'], m['r squared']) for m in models]
best_model = max(models_compared,key=lambda item:item[1])

for m in models:
    if m['model name'] == best_model[0]:
        final_model = m

with open('../models/models.pkl', 'wb') as f:
    pickle.dump(final_model, f)