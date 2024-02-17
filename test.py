import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Charger les variables d'environnement
load_dotenv('BDD_URL.env')
BDD_URL = os.environ['BDD_URL']
engine = create_engine(BDD_URL)

# Lire le fichier SQL
with open('sqlrequests/SQL.sql', 'r') as file:
    SQL = file.read()

# Charger les données depuis la base de données
df = pd.read_sql(SQL, engine)
if 'listesql' not in st.session_state:
    st.session_state['listesql'] = df

engine.dispose()

# Définition des fonctions
def BooleanToText(df):
    return df.apply(lambda x: 'True' if x == 1 else 'False')

def DateToCategory(df):
    df.fillna(df.mean(), inplace=True)
    bins = list(range(1800, 2056, 5))
    labels = [f"between{start}and{start+4}" for start in range(1800, 2051, 5)]
    return pd.cut(df, bins=bins, labels=labels, right=False)

def RuntimeToCategory(df):
    df.fillna(df.mean(), inplace=True)
    bins = list(range(0, 615, 15))
    labels = [f"runtime_Between{start}and{start+4}" for start in range(0, 600, 15)]
    return pd.cut(df, bins=bins, labels=labels, right=False)

def RatingToCategory(df):
    df.fillna(df.mean(), inplace=True)
    bins = list(range(0, 12, 2))
    labels = ['*', '**', '***', '****', '*****']
    return pd.cut(df, bins=bins, labels=labels, right=False)

def listTostr(df):
    return df.apply(lambda x: ' '.join(map(str, x)))

# Création des features
df['feature'] = df['primaryTitle'] + ' '
df['feature'] += 'titleType_' + df['titleType'] + ' '
df['feature'] += 'Rating_' + RatingToCategory(df['averageRating']).astype(str) + ' '
df['feature'] += 'startYear_' + DateToCategory(df['startYear']).astype(str) + ' '
df['feature'] += RuntimeToCategory(df['runtimeMinutes']).astype(str) + ' '
df['feature'] += 'genre_' + df['genres'].astype(str) + ' '
df['feature'] += 'ADULT_' + BooleanToText(df['isAdult']).astype(str) + ' '
df['feature'] += listTostr(df['Cate&names']).astype(str) + ' '
df['feature'][0]

# Vectorisation
cv = CountVectorizer()
count_matrix = cv.fit_transform(df['feature'])
cosine_sim = cosine_similarity(count_matrix)

# Fonctions de recommandation
def findfilm(index):
    return df.iloc[index][['tconst', 'primaryTitle']].tolist()

def getindex(filmm):
    return df[df['primaryTitle'] == filmm].index[0]

def Indexliste(array, listlent):
    R = list(enumerate(array, 0))
    sort_R = sorted(R, key=lambda x: x[1], reverse=True)
    sort_R = sort_R[1:listlent+1]
    return sort_R

def recommend(matrice=cosine_sim, film='', Nbfilm=5):
    indexfilm = getindex(film)
    vecteursimilarite = matrice[indexfilm]
    liste = Indexliste(vecteursimilarite, Nbfilm)
    rekomand = [findfilm(movie[0]) for movie in liste]
    return rekomand

# Interface Streamlit
st.title("Recommandeur de films")
st.write(df)

filmvoulu = st.text_input("Entrez le titre du film :", "")

if filmvoulu:
    recommendations = recommend(film=filmvoulu, Nbfilm=10)
    st.write("Les recommandations sont :")
    for recommendation in recommendations:
        st.write(recommendation[1])