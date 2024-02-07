import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

chunktaille = 100000
VarSchema = "Commun"

load_dotenv('BDD_URL.env')
BDD_URL = os.environ['BDD_URL']
engine = create_engine(BDD_URL)

def lirecsv(a):
    dff= pd.read_csv(f'BD/{a}.tsv', sep='\t', na_values='\\N', chunksize=chunktaille)
    for df in dff :
        print(a, df.shape)
        df.to_sql(a, con=engine, schema=VarSchema, if_exists='append', index=False)

tablenames = ['title_ratings', 'title_episode', 'title_crew', 'title_basics', 'name_basics', 'title_akas', 'title principals']

for tables in tablenames :
    lirecsv(tables)