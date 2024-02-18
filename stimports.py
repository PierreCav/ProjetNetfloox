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