#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 14:05:33 2024

@author: pierrecavallo
"""

import pandas as pd
from sqlalchemy import create_engine

BDD_URL='sqlite:////Users/pierrecavallo/Desktop/Projet Netfloox/ProjetNetfloox.sqlite'
connexion = create_engine(BDD_URL)

SQL= "SELECT deathYear, birthYear FROM df_name_basics"
df = pd.read_sql(SQL, connexion)
print(df)