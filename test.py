import pandas as pd
import numpy as np
import csv
import sqlite3

dbpath = str(input('path_de_votre_base_de_donnees.db : '))
table = str(input('nom_de_votre_table : '))
csvgen = 'newfile.csv'

def dbimport(a, b, c):
    connexion = sqlite3.connect(a)
    curseur = connexion.cursor()
    request = f"SELECT * FROM {b} LIMIT 10000"
    curseur.execute(request)
    resultats = curseur.fetchall()

    for ligne in resultats:
        print(ligne)
    connexion.close()

    with open(c, 'w', newline='', encoding='utf-8') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow([description[0] for description in curseur.description])
        writer.writerows(resultats)

dbimport(dbpath, table, csvgen)

#csv1 = "ProjetNetfloox\tsv\name_basics.tsv"
#csv2 = "ProjetNetfloox\tsv\title_akas.tsv"
#csv3 = "ProjetNetfloox\tsv\title_basics.tsv"
#csv4 = "ProjetNetfloox\tsv\title_crew.tsv"
#csv5 = "ProjetNetfloox\tsv\title_episode.tsv"
#csv6 = "ProjetNetflook\tsv\title_principals.tsv"
#csv7 = "ProjetNetfloox\tsv\title_ratings.tsv"

#df1 = pd.read_csv(csv1, sep='\t', header=None)
#df2 = pd.read_csv(csv2, sep='\t', header=None)
#df3 = pd.read_csv(csv3, sep="\t", header=None)
#df4 = pd.read_csv(csv4, sep='\t', header=None)

#dataframes = [df1, df2, df3, df4]