import pandas as pd
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv
load_dotenv('BDD_URL.env') # load environment variables from.env file

BDD_URL = os.environ['BDD_URL'] # get environment variable
print('BDD_URL=', BDD_URL)

engine = create_engine(BDD_URL)


SQL= """SELECT * 
        FROM mohammed.title_ratings 
        ;"""

df1 = pd.read_sql(SQL, engine)
print(df1)