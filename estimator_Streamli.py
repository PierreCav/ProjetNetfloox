import streamlit as st
import joblib
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



st.image('logo.png', use_column_width="auto")


# Interface utilisateur pour saisir les informations du film

def user_input_features():
    st.sidebar.header('Informations sur le film')
    primaryTitle = st.sidebar.text_input('Titre', value='6 Gunn')
    titleType = st.sidebar.selectbox('Type de titre', ('movie', 'short', 'tvMovie', 'video', 'tvShort', 'tvSpecial', 'videoGame', 'tvSeries', 'tvMiniSerie'))
    isAdult = st.sidebar.slider('Est pour adulte', 0, 1, 0)
    startYear = st.sidebar.slider('Année de début', 1800, 2050, 2014)
    runtimeMinutes = st.sidebar.slider('Durée en minutes', 1, 500, 116)
    genres = st.sidebar.text_input('genres', value='Drama')
    directors = st.sidebar.text_input('Directeurs', value='Kiran_Gawade')
    writers = st.sidebar.text_input('Scénaristes', value='Kiran_Gawade')
    actor = st.sidebar.text_input('Acteurs', value='Bhushan_Pradhan Devadhar_Archit')
    producer = st.sidebar.text_input('Producteurs', value='Abhishek_Jathar Ujjwala_Gawde')
    cinematographer = st.sidebar.text_input('cinematographer', value='missing')
    editor = st.sidebar.text_input('editor', value='missing')
    production_designer = st.sidebar.text_input('production designer', value='missing')
    self = st.sidebar.text_input('self', value='missing')
    archive_footage = st.sidebar.text_input('archive_footage', value='missing')
    archive_sound = st.sidebar.text_input('archive_sound', value='missing')

    
    data = {
        'primaryTitle': primaryTitle,
        'titleType': titleType,
        'isAdult': isAdult,
        'startYear': startYear,
        'runtimeMinutes': runtimeMinutes,
        'genres': genres,
        'directors': directors,
        'writers': writers,
        'actor': actor,
        'producer': producer,
        'cinematographer': cinematographer,
        'editor': editor,
        'production_designer': production_designer,
        'self': self,
        'archive_footage': archive_footage,
        'archive_sound': archive_sound,
       
    }
    features = pd.DataFrame(data, index=[0])
    features['isAdult']=features['isAdult'].astype(int)
    return features

# Affichage des informations saisies par l'utilisateur
st.title('Estimation de la popularité d\'un film')

user_input = user_input_features()

st.header('Informations saisies:')
st.table(user_input)

# Prédiction de la popularité avec les modèles
st.header('Estimation de la popularité:')
def booleantrans (x):
    return x.astype(bool).values.reshape(-1, 1)

@st.cache_data
def chargemodel():
    # Chargez le modèle à partir du fichier sauvegardé
    # return joblib.load('SVR1.pkl')
    import pickle
    with open('model.pkl', 'rb') as f:
        return pickle.load(f)

model = chargemodel()

prediction = model.predict(user_input)#[0]
st.write("Estimation de la popularité: ",prediction)

