import pandas as pd
import numpy as np

csv1 = r"ProjetNetfloox\tsv\name_basics.tsv"
csv2 = r"ProjetNetfloox\tsv\title_akas.tsv"
csv3 = r"ProjetNetfloox\tsv\title_basics.tsv"
csv4 = r"ProjetNetfloox\tsv\title_crew.tsv"
csv5 = r"ProjetNetfloox\tsv\title_episode.tsv"
csv6 = r"ProjetNetflook\tsv\title_principals.tsv"
csv7 = r"ProjetNetfloox\tsv\title_ratings.tsv"

df1 = pd.read_csv(csv1, sep='\t', header=None)
df2 = pd.read_csv(csv2, sep='\t', header=None)
df3 = pd.read_csv(csv3, sep="\t", header=None)
df4 = pd.read_csv(csv4, sep='\t', header=None)

dataframes = [df1, df2, df3, df4]