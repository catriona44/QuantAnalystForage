import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

def initialise_model():
    df = pd.read_csv('Nat_Gas.csv')
    df['Dates'] = pd.to_datetime(df['Dates'], format='%m/%d/%y')
    df['Year'] = df['Dates'].apply(lambda x: x.year)
    df['Season'] = df['Dates'].apply(lambda x: (x - datetime.datetime(x.year, 1, 1)) / datetime.timedelta(days=1))
    df['Season2'] = df['Season'].apply(lambda x: x ** 2)
    df['Season3'] = df['Season'].apply(lambda x: x ** 3)

    X = df[['Year', 'Season', 'Season2', 'Season3']]
    y = df['Prices']
    model = linear_model.LinearRegression()
    model.fit(X.values, y.values)
    return model


def predict(model, day: datetime) -> float:
    season = (day - datetime.datetime(day.year, 1, 1)) / datetime.timedelta(days=1)
    return model.predict([[day.year, season, season ** 2, season ** 3]])

'''
model = initialise_model()
mymodel = list(map(predict, df['Dates']))

plt.scatter(df.Dates, df.Prices)
plt.plot(df.Dates, mymodel)
plt.show()
'''
