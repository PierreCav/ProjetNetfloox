
#Chargement des données
# Data
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os 
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import math
# Graphics
import seaborn as sns 

from sklearn.experimental import enable_halving_search_cv # noqa

from sklearn.model_selection import HalvingGridSearchCV
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, RobustScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import FunctionTransformer
# from sklearn.metrics import root_mean_squared_error

# +
load_dotenv('BDD_URL.env')
BDD_URL = os.environ['BDD_URL']
engine = create_engine(BDD_URL)

SQL= """
SET search_path to principal;
SELECT  "primaryTitle", "titleType", "isAdult", "startYear", "runtimeMinutes", "genres", "averageRating", "directors", "writers", "actor", "producer", "cinematographer", "composer", "editor", "production_designer", "self", "archive_footage", "archive_sound"
from "castview"
where "runtimeMinutes" < 380 and "runtimeMinutes" Is NOT null and "averageRating" is NOT NULL and "genres" is NOT NULL and "startYear" is NOT NULL and "isAdult" is NOT NULL  and "directors" is NOT NULL and  "writers" is NOT NULL  and  "actor" is NOT NULL  and  "producer" is NOT NULL
ORDER BY "tconst" desc
limit 10000;
"""

#and "titleType" = 'movie' 

df = pd.read_sql(SQL, engine)
engine.dispose()


def liste_en_texte(lst):
    if isinstance(lst, list):
        return ' '.join(lst)
    else:
        return lst


def cleanText(df):
    df.fillna('missing', inplace=True)
    df=df.str.replace(',', ' ')
    return df


# +
columns_to_clean = ['primaryTitle', 'titleType', 'genres', 'directors', 'writers', 
                    'actor', 'producer', 'cinematographer', 'composer', 'editor', 
                    'production_designer', 'self', 'archive_footage', 'archive_sound']

for column in columns_to_clean:
    df[column] = cleanText(df[column])
# -


# +
# Séparation des caractéristiques et de la cible
X = df.drop(columns=["averageRating"])
# X = df[['genres','actor']]
y = df["averageRating"]

# Séparation des données d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# -

# Définition des colonnes numériques, textuelles et de description
numeric_features = ['startYear', 'runtimeMinutes']
boolean_features = 'isAdult'
text_features = ['titleType']

# +
# Création des transformers pour les colonnes numériques, booléennes, textuelles et de description
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', RobustScaler())
])

boolean_transformer = FunctionTransformer(lambda x: x.astype(bool).values.reshape(-1, 1)) 

text_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

Vect_transformer = Pipeline([
    # ('imputer', SimpleImputer(strategy='constant', fill_value='missing')), 
    ('vect', CountVectorizer(decode_error='ignore', analyzer='word')) #max_features=1000, analyzer="word"
])
tfidf_transformer = Pipeline([
    # ('imputer', SimpleImputer(strategy='constant', fill_value='missing')), 
    ('tf_idf', TfidfVectorizer(decode_error='ignore',analyzer='word')) #max_features=1000, sublinear_tf=True
])
# Création d'un ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('bool', boolean_transformer, boolean_features),
        # ('text', text_transformer, text_features), # c'est titleType
        
        ('title', Vect_transformer, 'primaryTitle'), 
        
        ('genres', tfidf_transformer, 'genres'),
        ('producer', tfidf_transformer, 'producer'),       
        ('directors', tfidf_transformer, 'directors'),
        ('writers', tfidf_transformer, 'writers'),
        ('actor', tfidf_transformer, 'actor'),

        ('cinematographer', tfidf_transformer, 'cinematographer'),
        ('composer', tfidf_transformer, 'composer'),
        ('editor', tfidf_transformer, 'editor'),
        ('production_designer', tfidf_transformer, 'production_designer'),
        ('selfy', tfidf_transformer, 'self'),
        ('archive_footage', tfidf_transformer, 'archive_footage'),
        ('archive_sound', tfidf_transformer, 'archive_sound')
        
        
    ])
preprocessor

# +
# Création des pipelines pour chaque modèle
pipelines = {
    'Linear Regression': Pipeline([('preprocessor', preprocessor), ('regressor', LinearRegression())]),
    'Ridge Regression': Pipeline([('preprocessor', preprocessor), ('regressor', Ridge())]),
    'Lasso Regression': Pipeline([('preprocessor', preprocessor), ('regressor', Lasso())]),
    'ElasticNet': Pipeline([('preprocessor', preprocessor), ('regressor', ElasticNet())]),
     'Random Forest Regression': Pipeline([('preprocessor', preprocessor), ('regressor', RandomForestRegressor())]),
    'Gradient Boosting Regression': Pipeline([('preprocessor', preprocessor), ('regressor', GradientBoostingRegressor())]),
    'SVR': Pipeline([('preprocessor', preprocessor), ('regressor', SVR())]),
}

# Paramètres pour GridSearchCV pour chaque modèle
parameters = {
    'Linear Regression': {'regressor__fit_intercept': [True,False]},
    'Ridge Regression': {'regressor__alpha': [0.1, 1.0, 5.0,10]},
    'Lasso Regression': {'regressor__alpha': [0.1, 1.0, 5.0,10]},
    'ElasticNet': {'regressor__alpha': [0.1, 1.0, 5.0,10], 'regressor__l1_ratio': [0.1, 0.5, 0.9]},
     'Random Forest Regression': {'regressor__n_estimators': [50,100], 'regressor__max_depth': [10, 20]},# None, 
    'Gradient Boosting Regression': {'regressor__n_estimators': [50,100], 'regressor__max_depth': [10, 20]},
    'SVR': {'regressor__kernel': ['linear', 'rbf'], 'regressor__C': [0.1, 1.0, 10.0]},
}

# Scoring : RMSE, R2 et MAE
scoring = {'RMSE': 'neg_root_mean_squared_error',
           'R2': 'r2',
           'MAE': 'neg_mean_absolute_error'}

# -

def Grid(X_train, y_train, pipeline, parameters, cv=5):


  # Grid search
  grid = GridSearchCV(pipeline, parameters,  scoring=scoring, refit='RMSE', cv=cv, n_jobs =-1, verbose = 0)#, error_score='raise'

  # Fit
  grid.fit(X_train, y_train)

  # Scores and results
  best_score = grid.best_score_.round(4)
  best_params = grid.best_params_
  training_time = grid.cv_results_['mean_fit_time'].mean().round(4)

  # Output
  return({
      'best_score': best_score,
      'best_params': best_params,
      'training_time': training_time,
      'fitted_model': grid.best_estimator_
  })


# +
def afficheResults (grid):
    model_name = grid['fitted_model'].named_steps['regressor'].__class__.__name__
    print(f"{model_name} training time: {grid['training_time']}")
    print(f"Best {model_name} parameters: {grid['best_params']}")
    print(f"Best {model_name} score: {-grid['best_score']}")
 
    
    

# +
# Boucle sur les modèles pour ajuster avec GridSearchCV
models = {}

# Boucle sur les modèles pour ajuster avec GridSearchCV et évaluation
for model_name, pipeline in pipelines.items():
    print(f"\n..............{model_name}..............................")
    grid_search = Grid(X_train, y_train, pipeline, parameters[model_name], cv=5)
    afficheResults (grid_search)
    
    best_model = grid_search['fitted_model']
    y_pred = best_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    Rmse = round(math.sqrt(mse), 4)
    models[model_name] = [best_model,Rmse]
    print(f"{model_name} RMSE: {Rmse}")

# +
# Trier les modèles par score RMSE croissant
sorted_models = sorted(models.items(), key=lambda x: x[1][1])

# Extraire les noms des modèles et les scores RMSE triés
model_names = [model[0] for model in sorted_models]
rmse_scores = [model[1][1] for model in sorted_models]


# Créer le graphique à barres
plt.figure(figsize=(10, 6))
plt.bar(model_names, rmse_scores)
plt.xlabel('Modèles')
plt.ylabel('RMSE')
plt.title('Scores RMSE des différents modèles (ordre croissant)')
plt.xticks(rotation=45, ha='right')  # Rotation des étiquettes pour une meilleure lisibilité
plt.tight_layout()  # Ajustement automatique des marges
plt.show()
# -


