import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import seaborn as sns ; sns.set()
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def data_load():
    load_dotenv('BDD_URL.env')
    BDD_URL = os.environ['BDD_URL']
    engine = create_engine(BDD_URL)


    SQL= """
    SET search_path to principal;
    SELECT  "tconst", "primaryTitle", "titleType", "isAdult", "startYear", "runtimeMinutes", "genres", "averageRating", "directors", "writers", "actor", "producer", "cinematographer", "composer", "editor", "production_designer", "self", "archive_footage", "archive_sound"
    from "castview"
    where "titleType" = 'movie' and "runtimeMinutes" < 380 and "runtimeMinutes" Is NOT null and "averageRating" is NOT NULL and "genres" is NOT NULL and "startYear" is NOT NULL and "isAdult" is NOT NULL  and "directors" is NOT NULL and  "writers" is NOT NULL  and  "actor" is NOT NULL  and  "producer" is NOT NULL
    ORDER BY "tconst" desc
    limit 100;
    """
    df = pd.read_sql(SQL, engine)
    engine.dispose()
    return df
df = data_load()


def liste_en_texte(lst):
    if isinstance(lst, list):
        return ' '.join(lst)
    else:
        return lst
    
def cleanText(df):
    df.fillna('missing', inplace=True)
    df=df.str.replace(',', ' ')
    return df


columns_to_clean = ['primaryTitle', 'titleType', 'genres', 'directors', 'writers', 
                    'actor', 'producer', 'cinematographer', 'composer', 'editor', 
                    'production_designer', 'self', 'archive_footage', 'archive_sound']

for column in columns_to_clean:
    df[column] = cleanText(df[column])



def BooleanToText (df):
    return df.apply(lambda x: 'True' if x == 1 else 'False')


def DateToCategory (df):
    
    df.fillna(df.mean(), inplace=True) # a valider
    
    bins = list(range(1800, 2056, 5))  # Intervalles de 5
    labels = [f"between{start}and{start+4}" for start in range(1800, 2051, 5)]

    return pd.cut(df, bins=bins, labels=labels, right=False)



def RuntimeToCategory (df):
    
    df.fillna(df.mean(), inplace=True) # a valider
    
    bins = list(range(0, 615, 15))  # Intervalles de 10h
    labels = [f"runtime_Between{start}and{start+15}" for start in range(0, 600, 15)]

    return pd.cut(df, bins=bins, labels=labels, right=False) #qcut 


def RatingToCategory (df):
    
    df.fillna(df.mean(), inplace=True) # a valider
    
    bins = list(range(0, 12, 2))  
    labels = ['*','**','***','****','*****']

    return pd.cut(df, bins=bins, labels=labels, right=False)


def listTostr (df):
    return df.apply(lambda x: ' '.join(map(str, x)))


def crewmod (x, type):
    return ' '.join([type +'_'+ name for name in x.split()])


df['feature'] = df['primaryTitle'] + ' '

df['feature'] += 'titleType_'+df['titleType'] + ' '

df['feature'] += 'Rating_'+RatingToCategory(df['averageRating']).astype(str) + ' '

df['feature'] += 'startYear_'+DateToCategory(df['startYear']).astype(str) + ' '

df['feature'] += RuntimeToCategory (df['runtimeMinutes']).astype(str)+ ' '

df['feature'] += df['genres'] + ' '

df['feature'] += 'ADULT_'+BooleanToText (df['isAdult']).astype(str)+' '

df['feature'] += df['directors'].apply(crewmod, type='directors').astype(str)+' '
df['feature'] += df['writers'].apply(crewmod, type='writers').astype(str)+' '
df['feature'] += df['actor'].apply(crewmod, type='actor').astype(str)+' '
df['feature'] += df['producer'].apply(crewmod, type='producer').astype(str)+' '

df['feature'][0]
# -

cv = CountVectorizer(analyzer="word")
count_vect = cv.fit_transform(df['feature'])



def findfilm(index):
    if index < len(df):
        return df.iloc[index][['tconst', 'primaryTitle']].tolist()
    else:
        return None  


def getindex(filmm):
    index_list = df[df['primaryTitle'] == filmm].index
    if len(index_list) > 0:
        return index_list[0]
    else:
        return None

def Indexliste(array,listlent):
    R = list(enumerate(array, 0))
    sort_R=sorted(R, key=lambda x: x[1], reverse=True)
    sort_R=sort_R[1:listlent+1] # les 1 pour supprimer le film lui meme de la list des recommendations
    return sort_R




def recommend(film='' , Nbfilm=5):
    indexfilm = getindex(film)
    if indexfilm == None :
        return []
    
    vecteursimilarite = cosine_similarity(count_vect,count_vect[indexfilm])
    liste = Indexliste(vecteursimilarite, Nbfilm)
    # rekomand = [[movie[0],findfilm(movie[0]),round(movie[1],2)] for movie in liste]
    rekomand = [findfilm(movie[0]) for movie in liste]
    return rekomand


recommend(film='Wet Dog', Nbfilm=10)
