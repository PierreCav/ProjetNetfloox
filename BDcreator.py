#c'est pour creer la base de données avec toutes les tables completes
import pandas as pd
from sqlalchemy import create_engine
df_title_rating=pd.read_csv("BD/title_ratings.tsv", sep='\t',na_values='\\N')
df_title_episode=pd.read_csv("BD/title_episode.tsv", sep='\t',na_values='\\N')
df_title_crew=pd.read_csv("BD/title_crew.tsv", sep='\t',na_values='\\N')
df_title_basic=pd.read_csv("BD/title_basics.tsv", sep='\t',na_values='\\N')
df_name_basics=pd.read_csv("BD/name_basics.tsv", sep='\t',na_values='\\N')
df_title_akas=pd.read_csv("BD/title_akas.tsv", sep='\t',na_values='\\N')
df_title_akas.rename(columns={'titleId':'tconst'},inplace=True)
df_title_principals=pd.read_csv("BD/title_principals.tsv", sep='\t',na_values='\\N')

# Créez une connexion à la base de données
engine = create_engine('postgresql://citus:floox2024!@c-groupe2.jh4mqc5jxykkfg.postgres.cosmos.azure.com:5432/netfloox?sslmode=require')

VarSchema=""

#TITLE RATING
df_title_rating.to_sql('title_ratings', con=engine, schema=VarSchema, if_exists='replace', index=False)

#TITLE EPISODE
df_title_episode.to_sql('title_episode', con=engine, schema=VarSchema, if_exists='replace', index=False)

#TITLE CREW
df_title_crew.to_sql('title_crew', con=engine, schema=VarSchema, if_exists='replace', index=False)

#TITLE BASICS
df_title_basic.to_sql('title_basics', con=engine, schema=VarSchema, if_exists='replace', index=False)

#NAME BASICS
df_name_basics.to_sql('name_basics', con=engine, schema=VarSchema, if_exists='replace', index=False)

#TITLE_AKAS
df_title_akas.to_sql('title_akas', con=engine, schema=VarSchema, if_exists='replace', index=False)

#TITLE_PRINCIPALS
df_title_principals.to_sql('title_principals', schema=VarSchema, con=engine, if_exists='replace', index=False)

engine.dispose()



