import pandas as pd
import logging
import sqlite3
import sys, os

######################################

#working directory is Project_1 map

#relatief pad naar database
db_path = './rest_server/medisch_centrum_randstad/data/db.sqlite3'

######################################

#Verbinding maken met SQLite database
logging.info("Connecting to database")

db_connection = sqlite3.connect(db_path)
table_name = "rest_api_netlify"

logging.info("")
#Data in dataframe zetten
df = pd.read_sql_query(f"SELECT * FROM {table_name}", db_connection)


#We droppen de 'id' column
df.drop(['id'], axis=1, inplace=True)


#In het geval dat het dataframe values bevat die niet naar floats kunnen worden omgezet:
for c in df.columns:
    df[c] = pd.to_numeric(df[c], errors='coerce')

removed_rows = [i for i in df[df.isnull().any(axis=1)].index]

print(f'Dataframe contains {len(removed_rows)} rows with NaN values: {removed_rows}')


#Verwijderen van rijen met lege waardes in df:
df.dropna(inplace=True)

print(f'Dataframe is now of shape {df.shape} after dropping empty-cell rows.')


#Checken of waardes buiten 'normale' ranges vallen voor alle variabelen:
range_dict = {}

#Hier kunnen we de grenswaardes voor elke variabel vaststellen:

range_dict['genetic'] = (40, 120)
range_dict['length'] =(147, 220)
range_dict['mass'] = (50,175)
range_dict['exercise'] = (0,6)
range_dict['smoking'] = (0,25)
range_dict['alcohol'] = (0,7)
range_dict['lifespan'] = (40,120)
range_dict['sugar'] = (0,15)

#We halen alle waardes buiten de ranges uit het dataframe:

for c in df.columns:
    df = df[df[c].between(range_dict[c][0], range_dict[c][1])]

print(f'Dataframe is now of shape {df.shape} after dropping rows containing out-of-range cell values.')



#BMI kolom toevoegen
df['BMI'] = (df['mass'] / ((df['length'])/100)**2).round()
df['age_diff'] = round((df['lifespan'] - df['genetic']), 3)
df.drop(['mass', 'length', 'lifespan', 'genetic'], axis=1, inplace=True)


#Voeg een nieuwe table toe aan de database
df.to_sql('regression_table_2', con=db_connection, if_exists='replace', index=False)

#Connectie met database sluiten
db_connection.close()

print(df.corr())
