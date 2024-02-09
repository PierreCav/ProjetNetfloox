import pandas as pd
import sqlite3

df_title_rating=pd.read_csv("tsv/title_ratings.tsv", sep='\t',nrows=10000,na_values='\\N')
df_title_episode=pd.read_csv("tsv/title_episode.tsv", sep='\t',nrows=10000,na_values='\\N')
df_title_crew=pd.read_csv("tsv/title_crew.tsv", sep='\t',nrows=10000,na_values='\\N')
df_title_basic=pd.read_csv("tsv/title_basic.tsv", sep='\t',nrows=10000,na_values='\\N')
df_name_basics=pd.read_csv("tsv/name_basics.tsv", sep='\t',nrows=10000,na_values='\\N')
df_title_akas=pd.read_csv("tsv/title_akas.tsv", sep='\t',nrows=10000,na_values='\\N')
df_title_akas.rename(columns={'titleId':'tconst'},inplace=True)
df_title_principals=pd.read_csv("tsv/title_principals.tsv", sep='\t',nrows=10000,na_values='\\N')


con = sqlite3.connect("")
cur = con.cursor()

#TITLE RATING
cur.execute("DROP TABLE IF EXISTS df_title_rating")
cur.execute("CREATE TABLE df_title_rating (tconst TEXT, averagerating INTEGER, numVotes)")
df_title_rating.to_sql('df_title_rating', con, if_exists='append', index=False)

#TITLE EPISODE
cur.execute("DROP TABLE IF EXISTS df_title_episode")
cur.execute("CREATE TABLE df_title_episode (tconst TEXT, parentTconst TEXT, seasonNumber INTEGER, episodeNumber INTEGER)")
df_title_episode.to_sql('df_title_episode', con, if_exists='append', index=False)

#TITLE CREW
cur.execute("DROP TABLE IF EXISTS df_title_crew")
cur.execute("CREATE TABLE df_title_crew (tconst TEXT, directors TEXT, writers TEXT)")
df_title_crew.to_sql('df_title_crew', con, if_exists='append', index=False)

#TITLE BASICS
cur.execute("DROP TABLE IF EXISTS df_title_basic")
cur.execute("CREATE TABLE df_title_basic (tconst TEXT, titleType TEXT, primaryTitle TEXT, originalTitle TEXT, isAdult INTEGER, startYear INTEGER, endYear INTEGER, runtimeMinutes INTEGER, genres TEXT)")
df_title_basic.to_sql('df_title_basic', con, if_exists='append', index=False)

#NAME BASICS
cur.execute("DROP TABLE IF EXISTS df_name_basics")
cur.execute("CREATE TABLE df_name_basics (nconst TEXT, primaryName TEXT, birthYear INTEGER, deathYear INTEGER, primaryProfession TEXT, startYear INTEGER, knownForTitles TEXT)")
df_name_basics.to_sql('df_name_basics', con, if_exists='append', index=False)

#TITLE_AKAS
cur.execute("DROP TABLE IF EXISTS df_title_akas")
cur.execute("CREATE TABLE df_title_akas (tconst TEXT, ordering TEXT,title TEXT, region TEXT, language TEXT, types TEXT, attributes TEXT, isOriginalTitle INTEGER)")
df_title_akas.to_sql('df_title_akas', con, if_exists='append', index=False)

#TITLE_PRINCIPALS
cur.execute("DROP TABLE IF EXISTS df_title_principals")
cur.execute("CREATE TABLE df_title_principals (tconst TEXT, ordering INTEGER, nconst TEXT,category TEXT, job TEXT, characters TEXT)")
df_title_principals.to_sql('df_title_principals', con, if_exists='append', index=False)


con.close()