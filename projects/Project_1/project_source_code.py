import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

df = pd.read_csv('data_clean.csv', sep=';')

x = df[['exercise', 'smoking', 'alcohol', 'sugar', 'BMI']]
y = df['lifespan']


lin_model = LinearRegression()

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.8, random_state=42)

lin_model.fit(x_train, y_train)

pred = lin_model.predict(x_test)

print(mean_squared_error(y_test, pred))
print(mean_absolute_error(y_test, pred))