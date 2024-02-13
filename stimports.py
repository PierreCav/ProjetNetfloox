import streamlit as st
import os
from sqlalchemy import create_engine, Column, Integer
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from st_clickable_images import clickable_images

# Fonction pour importer la BDD avec le fichier environnement
def create_database_engine(env_file_path):
    load_dotenv(env_file_path)
    bdd_url = os.environ.get('BDD_URL')
    if bdd_url is None:
        raise ValueError("La variable d'environnement BDD_URL n'est pas définie dans le fichier .env")
    engine = create_engine(bdd_url)
    return engine

SQL_director_crewnames = """
SET search_path to principal;
SELECT "primaryTitle", "averageRating", "titleType", "startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers" , array_agg(name_basics."primaryName") AS director_names
        
        from title_basics 
        
        join title_ratings on title_basics."tconst" = title_ratings."tconst"
        
        join title_crew on title_basics."tconst" = title_crew."tconst"
        
        join name_basics on name_basics.nconst = ANY(string_to_array(title_crew."directors", ','))
        
        GROUP BY "primaryTitle", "averageRating", "titleType", "startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers"
        
        limit 2;
"""

SQL_SIMPLE = """
SET search_path to principal;
SELECT "primaryTitle", 
        "averageRating", 
        "titleType", 
        "startYear", 
        "runtimeMinutes", 
        "genres", 
        "isAdult", 
        "directors", 
        "writers"
        
        from title_basics 
        
        join title_ratings on title_basics."tconst" = title_ratings."tconst"
        
        join title_crew on title_basics."tconst" = title_crew."tconst"
        
        limit 10;
"""

SQL_filmview= """
SELECT tb.tconst,
    tb."primaryTitle",
    tb."titleType",
    tb."isAdult",
    tb."startYear",
    tb."endYear",
    tb."runtimeMinutes",
    tb.genres,
    rt."averageRating",
    rt."numVotes",
    array_agg((tp.category || '_'::text) || replace(nb."primaryName", ' '::text, '_'::text)) AS "Cate&names"
   FROM principal.title_basics tb
     JOIN principal.title_ratings rt ON tb.tconst::text = rt.tconst::text
     JOIN principal.title_principals tp ON tb.tconst::text = tp.tconst::text
     JOIN principal.name_basics nb ON tp.nconst::text = nb.nconst::text
  GROUP BY tb.tconst, rt."averageRating", rt."numVotes";

"""

SQL= """
SET search_path to principal;
SELECT *
from "filmview"
limit 10000;
"""