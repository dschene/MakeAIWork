import pandas as pd
import logging
import sqlite3
from pathlib import Path

######################################

#relatief pad naar database
db_path = '../rest_server/medisch_centrum_randstad/data/db.sqlite3'
logging.basicConfig(level=logging.INFO)

######################################

#Verbinding maken met SQLite database
logging.info(f"Connecting to database {Path(db_path).name}")

db_connection = sqlite3.connect(db_path)
table_name = "rest_api_netlify"

#Data in dataframe zetten
logging.info("Loading data from database into dataframe")
df = pd.read_sql_query(f"SELECT * FROM {table_name}", db_connection)

#We droppen de 'id' column
df.drop(['id'], axis=1, inplace=True)

#In het geval dat het dataframe values bevat die niet naar floats kunnen worden omgezet maken we deze cellen leeg:
for c in df.columns:
    df[c] = pd.to_numeric(df[c], errors='coerce')

#Van de rijen met lege waardes slaan we de index op in een lijst, voor onze administratie bij wijze van spreken:
removed_rows = [i for i in df[df.isnull().any(axis=1)].index]

logging.info(f'Dataframe contains {len(removed_rows)} rows with NaN values: {removed_rows}')


logging.info("Preprocessing: removing rows containting NaN values")
#Verwijderen van rijen met lege waardes in df:
df.dropna(inplace=True)

logging.info(f'Dataframe is now of shape {df.shape} after dropping empty-cell rows.')


#Voor het vaststellen van de limieten maken we een dictionary 
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
logging.info("Preprocessing: removing rows containing out-of-range values.")
for c in df.columns:
    df = df[df[c].between(range_dict[c][0], range_dict[c][1])]

logging.info(f'Dataframe is now of shape {df.shape} after dropping rows containing out-of-range cell values.')

logging.info("Feature engineering: creating a BMI variable and BMI labels")
#BMI kolom toevoegen
df['BMI'] = (df['mass'] / ((df['length'])/100)**2).round()

#We maken een nieuwe kolom aan met daarin het verschil tussen iemands lifespan en de genetische leeftijd. 
df['age_diff'] = round((df['lifespan'] - df['genetic']), 3)

#Verwijderen van kolommen die we voor deze nieuwe versie van het model niet nodig hebben
df.drop(['mass', 'length', 'lifespan', 'genetic'], axis=1, inplace=True)

logging.info("Storing new data in new database table")
#Voeg een nieuwe table toe aan de database, met hierin de data die klaar is voor gebruik met ons model
df.to_sql('regression_table_2', con=db_connection, if_exists='replace', index=False)

#Connectie met database sluiten
db_connection.close()
logging.info("Process complete - closing connection with database")