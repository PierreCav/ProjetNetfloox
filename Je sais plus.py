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
import seaborn as sns ; sns.set()

# Graphics
import seaborn as sns ; sns.set()

# Machine learning - Preprocessing
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import ColumnTransformer

# Machine learning - Automatisation
from sklearn.pipeline import Pipeline
from sklearn import set_config

# Machine learning - Models
from sklearn.linear_model import LogisticRegression, LinearRegression

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, HistGradientBoostingClassifier
from sklearn.naive_bayes import ComplementNB, GaussianNB, MultinomialNB

# Machine learning - Model selection
from sklearn.model_selection import train_test_split, GridSearchCV

# Machine learning - Metrics
from sklearn import metrics
from sklearn.metrics import confusion_matrix, accuracy_score, ConfusionMatrixDisplay, f1_score, fbeta_score, recall_score, fbeta_score, make_scorer, roc_curve
from sklearn.preprocessing import LabelEncoder


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
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import RobustScaler



load_dotenv('BDD_URL.env')
BDD_URL = os.environ['BDD_URL']
engine = create_engine(BDD_URL)

SQL = 'SELECT "averageRating", "startYear", "runtimeMinutes" from principal.title_basics join principal.title_ratings on principal.title_basics."tconst" = principal.title_ratings."tconst"  limit 50000;'
df = pd.read_sql(SQL, engine)

df["averageRating"].fillna(df["averageRating"].mean(), inplace=True)
df["startYear"].fillna(df["startYear"].mean(), inplace=True)
df["runtimeMinutes"].fillna(df["runtimeMinutes"].mean(), inplace=True)

y=df['averageRating']
X=df[['startYear','runtimeMinutes']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25,
random_state=42)

def crossval_paramsearch(X_train, y_train, estimator, parameters, cv=5):
  # Scoring
  #multi_scoring = {mean_squared_error,r2_score}
    
    
  # Grid search
  grid = GridSearchCV(estimator=estimator, param_grid=parameters,
                      scoring='neg_mean_squared_error',
                      cv=cv, n_jobs=-1, verbose=1, error_score="raise")

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

#Fonction pipeline

def pipefilm(regressor=LinearRegression()):

  # Données numériques
  pipe_num = Pipeline(steps=[
       ('minmax', MinMaxScaler())
       ])

  # Transformation des données
  # Class ColumnTransformer : apply alls steps on the whole dataset
  preparation = ColumnTransformer(
      transformers=[
        ('scaler', pipe_num , ['startYear', 'runtimeMinutes']),
        ],
      remainder='passthrough'
)


  # Intégration du pipeline de preprocessing avec un modèle de classification
  pipe = Pipeline(steps=[
       ('prep', preparation),
       ('rgr', regressor)
       ])

  return pipe


#Preprocessing


#df.describe()
#df.info()
#Capiccino?


parameters = [{
        # Params for Linear
        'fit_intercept': [True,False]
        #'prep__vectorizer__countvect': [CountVectorizer()],
        #'prep__vectorizer__countvect__ngram_range' : [(1, 1), (1, 2), (1, 3), (1, 4)],
        #'prep__vectorizer__countvect__max_features': [500, 1000, 3000, 5000, 8000, None],

        # Params for numeric MinMaxScaling
        #prep__scaler__minmax__feature_range': [(0, 1), (0, 10)],
        }]

print(crossval_paramsearch(X_train=X_train, y_train=y_train, estimator=LinearRegression(),parameters=parameters,cv=5))
