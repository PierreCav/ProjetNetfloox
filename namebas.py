import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

chunktaille = 100000
VarSchema = "principal"

load_dotenv('BDD_URL.env')
BDD_URL = os.environ['BDD_URL']
engine = create_engine(BDD_URL)

df_lol = pd.read_csv('BD/t.tsv', sep='\t', na_values='\\N')

df_lol.to_sql('title_akas.tsv', con=engine, schema=VarSchema, if_exists='replace', index=False)

engin.dispose()
