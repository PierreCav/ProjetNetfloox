#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 13:38:37 2024

@author: pierrecavallo
"""

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import seaborn as sns ; sns.set()
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import RobustScaler

load_dotenv('BDD_URL.env')
BDD_URL = os.environ['BDD_URL']
engine = create_engine(BDD_URL)

SQL = '''SELECT "averageRating", "startYear", "runtimeMinutes" from principal.title_basics join principal.title_ratings on principal.title_basics."tconst" = principal.title_ratings."tconst"  limit 50000;'''
df = pd.read_sql(SQL, engine)
df


# Création de la partition train / test
y=df['averageRating']
X=df[['startYear','runtimeMinutes']]

# Traiter les valeurs manquantes
X.fillna(X.mean(), inplace=True)
y.fillna(y.mean(), inplace=True)



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25,
random_state=42)

scaler = RobustScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Déclaration du modèle
model = LinearRegression()

# Entrainement du modèle
model.fit(X_train, y_train)

# Prédiction sur nouvelles valeurs
y_pred = model.predict(X_test)

# Accès au score 

print('score =',model.score(X_train, y_train))

# Accès au score 
print('R2 =',r2_score(y_test, y_pred))

mse = mean_squared_error(y_test, y_pred)
print("MSE = ", mse)

rmse = np.sqrt(mse)
print("RMSE =", rmse)

# Calculer l'erreur absolue moyenne (MAE)
mae = mean_absolute_error(y_test, y_pred)
print("MAE =", mae)




