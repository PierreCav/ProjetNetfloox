import streamlit as st
from streamlit_option_menu import option_menu
import st_clickable_images as stc
from st_clickable_images import clickable_images
import os
import re
import difflib
from PIL import Image
import requests
from sqlalchemy import create_engine, Column, Integer
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from st_clickable_images import clickable_images
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns ; sns.set()
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import numpy as np
import math
from sklearn.experimental import enable_halving_search_cv
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

# Fonction pour importer la BDD avec le fichier environnement
def create_database_engine(env_file_path):
    load_dotenv(env_file_path)
    bdd_url = os.environ.get('BDD_URL')
    if bdd_url is None:
        raise ValueError("La variable d'environnement BDD_URL n'est pas définie dans le fichier .env")
    engine = create_engine(bdd_url)
    return engine

# Fonction pour récupérer l'URL de la jaquette d'un film à partir de TMDb
def get_movie_poster_url(tmdb_id):
    api_key = '330f02856761de4af7dcfbad30b193ae'
    base_url = 'https://api.themoviedb.org/3/movie/'
    endpoint = f'{tmdb_id}?api_key={api_key}'
    response = requests.get(base_url + endpoint)
    if response.status_code == 200:
        data = response.json()
        if 'poster_path' in data:
            poster_path = data['poster_path']
            return f'https://image.tmdb.org/t/p/w500/{poster_path}'
    return None

def get_movie_synopsis(tmdb_id):
    api_key = '330f02856761de4af7dcfbad30b193ae'
    base_url = 'https://api.themoviedb.org/3/movie/'
    endpoint = f'{tmdb_id}?api_key={api_key}&language=fr-FR'  # Modifier la langue si nécessaire
    response = requests.get(base_url + endpoint)
    if response.status_code == 200:
        data = response.json()
        if 'overview' in data:
            return data['overview']
    return None