import pandas as pd
from sqlalchemy import create_engine
import psycopg2

host = "host=c-groupe2.jh4mqc5jxykkfg.postgres.cosmos.azure.com"
database = "netfloox"
user = "citus"
password = "floox2024!"
sslmode = "require"

# Créez une connexion à la base de données
con = psycopg2.connect(
    dbname=database,
    user=user,
    password=password,
    host=host,
    sslmode=sslmode
)



""" BDD_URL='sqlite:////Users/pierrecavallo/Desktop/Projet Netfloox/ProjetNetfloox.sqlite'
connexion = create_engine(BDD_URL)

SQL= "SELECT deathYear, birthYear FROM df_name_basics"
df = pd.read_sql(SQL, connexion)
print(df) """