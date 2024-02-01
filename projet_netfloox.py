#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 16:20:32 2024

@author: pierrecavallo
"""
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

df_title_rating=pd.read_csv("title_rating.tsv", sep='\t',nrows=10000,na_values='\\N')
df_title_episode=pd.read_csv("title_episode.tsv", sep='\t',nrows=10000,na_values='\\N')
df_title_crew=pd.read_csv("title_crew.tsv", sep='\t',nrows=10000,na_values='\\N')
df_title_basic=pd.read_csv("title_basic.tsv", sep='\t',nrows=10000,na_values='\\N')
df_name_basics=pd.read_csv("name_basics.tsv", sep='\t',nrows=10000,na_values='\\N')
df_title_akas=pd.read_csv("title_akas.tsv", sep='\t',nrows=10000,na_values='\\N')
df_title_akas.rename(columns={'titleId':'tconst'},inplace=True)
df_title_principals=pd.read_csv("title_principals.tsv", sep='\t',nrows=10000,na_values='\\N')

# Créez une connexion à la base de données
engine = create_engine('postgresql://citus:floox2024!@c-groupe2.jh4mqc5jxykkfg.postgres.cosmos.azure.com:5432/netfloox?sslmode=require')

#TITLE RATING
df_title_rating.to_sql('df_title_rating', con=engine, schema="Pierre", if_exists='replace', index=False)

#TITLE EPISODE
df_title_episode.to_sql('df_title_episode', con=engine, schema="Pierre", if_exists='replace', index=False)

#TITLE CREW
df_title_crew.to_sql('df_title_crew', con=engine, schema="Pierre", if_exists='replace', index=False)

#TITLE BASICS
df_title_basic.to_sql('df_title_basic', con=engine, schema="Pierre", if_exists='replace', index=False)

#NAME BASICS
df_name_basics.to_sql('df_name_basics', con=engine, schema="Pierre", if_exists='replace', index=False)

#TITLE_AKAS
df_title_akas.to_sql('df_title_akas', con=engine, schema="Pierre", if_exists='replace', index=False)

#TITLE_PRINCIPALS
df_title_principals.to_sql('df_title_principals', schema="Pierre", con=engine, if_exists='replace', index=False)


engine.dispose()



