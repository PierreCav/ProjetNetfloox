from stimports import *

# Onglet de la page
st.set_page_config(
    page_title="Netfloox - Recommandation",
    page_icon="🍿"
)

# Ecran titre avec logo
image = "ressources/title.png"
st.image(image, caption=None, width=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
st.markdown("<h2 style='text-align: center;'>&#127871 ON REGARDE QUOI CE SOIR ?	&#127871</h2>", unsafe_allow_html=True)
st.write("")

# Initialisation des valeurs session
if "explicit_content" not in st.session_state:
    st.session_state["explicit_content"] = False

if "selected_title" not in st.session_state:
    st.session_state['selected_title'] = None

if 'clicked_index' not in st.session_state:
    st.session_state['clicked_index'] = None

@st.cache_data
def data_load():
    load_dotenv('BDD_URL.env')
    BDD_URL = os.environ['BDD_URL']
    engine = create_engine(BDD_URL)

    SQL= """
    SET search_path to principal;
    SELECT  "tconst", "primaryTitle", "titleType", "isAdult", "startYear", "runtimeMinutes", "genres", "averageRating", "directors", "writers", "actor", "producer", "cinematographer", "composer", "editor", "production_designer", "self", "archive_footage", "archive_sound", "numVotes"
    from "castview"
    where "runtimeMinutes" < 380
    ORDER BY "numVotes" DESC NULLS LAST, "averageRating" DESC NULLS LAST
    limit 100000;
    """
    df = pd.read_sql(SQL, engine)
    engine.dispose()
    return df

df = data_load()

df_filtered = ''
selectedc = ''

st.sidebar.title("Catégorie")
categories = ['Films', "Séries"]
selected_category = st.sidebar.radio("Sélectionner une catégorie", categories)
checkboite = st.sidebar.checkbox("Contenu explicite", key="disabled")
st.session_state["explicit_content"] = checkboite

if selected_category == 'Films':
    df_filtered = df[(df['titleType'] == 'movie') & (df['isAdult'] == st.session_state['explicit_content'])]
    selectedc = 'Films'
elif selected_category == 'Séries':
    df_filtered = df[df['titleType'] == 'tvSeries']
    selectedc = 'Séries'

placeholdertitre = st.empty()
placeholder = st.empty()
placeholdermdr = st.empty()
placeholder2 = st.empty()

st.markdown("---")
st.write("")

def liste_en_texte(lst):
    if isinstance(lst, list):
        return ' '.join(lst)
    else:
        return lst
    
def cleanText(df_filtered):
    df_filtered.fillna('missing', inplace=True)
    df_filtered=df_filtered.str.replace(',', ' ')
    return df_filtered


columns_to_clean = ['primaryTitle', 'titleType', 'genres', 'directors', 'writers', 
                    'actor', 'producer', 'cinematographer', 'composer', 'editor', 
                    'production_designer', 'self', 'archive_footage', 'archive_sound']

for column in columns_to_clean:
    df_filtered[column] = cleanText(df_filtered[column])



def BooleanToText (df_filtered):
    return df_filtered.apply(lambda x: 'True' if x == 1 else 'False')


def DateToCategory (df_filtered):
    
    df_filtered.fillna(df_filtered.mean(), inplace=True) # a valider
    
    bins = list(range(1800, 2056, 5))  # Intervalles de 5
    labels = [f"between{start}and{start+4}" for start in range(1800, 2051, 5)]

    return pd.cut(df_filtered, bins=bins, labels=labels, right=False)



def RuntimeToCategory (df_filtered):
    
    df_filtered.fillna(df_filtered.mean(), inplace=True) # a valider
    
    bins = list(range(0, 615, 15))  # Intervalles de 10h
    labels = [f"runtime_Between{start}and{start+15}" for start in range(0, 600, 15)]

    return pd.cut(df_filtered, bins=bins, labels=labels, right=False) #qcut 


def RatingToCategory (df_filtered):
    
    df_filtered.fillna(df_filtered.mean(), inplace=True) # a valider
    
    bins = list(range(0, 12, 2))  
    labels = ['*','**','***','****','*****']

    return pd.cut(df_filtered, bins=bins, labels=labels, right=False)


def listTostr (df_filtered):
    return df_filtered.apply(lambda x: ' '.join(map(str, x)))


def crewmod (x, type):
    return ' '.join([type +'_'+ name for name in x.split()])


df_filtered['feature'] = df_filtered['primaryTitle'] + ' '

df_filtered['feature'] += 'titleType_'+df_filtered['titleType'] + ' '

df_filtered['feature'] += 'Rating_'+RatingToCategory(df_filtered['averageRating']).astype(str) + ' '

df_filtered['feature'] += 'startYear_'+DateToCategory(df_filtered['startYear']).astype(str) + ' '

df_filtered['feature'] += RuntimeToCategory (df_filtered['runtimeMinutes']).astype(str)+ ' '

df_filtered['feature'] += df_filtered['genres'] + ' '

df_filtered['feature'] += 'ADULT_'+BooleanToText (df_filtered['isAdult']).astype(str)+' '

df_filtered['feature'] += df_filtered['directors'].apply(crewmod, type='directors').astype(str)+' '
df_filtered['feature'] += df_filtered['writers'].apply(crewmod, type='writers').astype(str)+' '
df_filtered['feature'] += df_filtered['actor'].apply(crewmod, type='actor').astype(str)+' '
df_filtered['feature'] += df_filtered['producer'].apply(crewmod, type='producer').astype(str)+' '


cv = CountVectorizer(analyzer="word")
count_vect = cv.fit_transform(df_filtered['feature'])

def findfilm(index):
    if index < len(df_filtered):
        return df_filtered.iloc[index][['tconst', 'primaryTitle']].tolist()
    else:
        return None  

def getindex(filmm):
    index_list = df_filtered[df_filtered['primaryTitle'] == filmm].index
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
    # rekomand = [[movie[0],findf_filteredilm(movie[0]),round(movie[1],2)] for movie in liste]
    rekomand = [findfilm(movie[0]) for movie in liste]
    return rekomand


# Fonction de rendu d'images cliquables
def render_images(tmdb_ids, movie_titles, max_images=10):
    if tmdb_ids is not None and movie_titles is not None:
        for i in range(0, min(len(tmdb_ids), max_images), 4):
            cols = st.columns(4)
            for j in range(4):
                index = i + j
                if index < len(tmdb_ids):
                    tmdb_id = tmdb_ids[index]
                    movie_title = movie_titles[index]
                    poster_url = get_movie_poster_url(tmdb_id)
                    filmsynopsis = get_movie_synopsis(tmdb_id)
                    if poster_url:
                        with cols[j]:
                            st.session_state['clicked_index'] = clickable_images(
                                [poster_url],
                                titles=[movie_title],
                                div_style={"display": "flex", "justify-content": "center"},
                                img_style={"margin": "5px", "height": "200px"},
                            )
                            st.write(movie_title)
                            if st.session_state['clicked_index'] > -1:
                                placeholdertitre.markdown(f"<h3 style='text-align: center;'> Synopsis : {movie_title} </h3>", unsafe_allow_html=True)
                                placeholder.write(filmsynopsis)
                                placeholdermdr.markdown("<h3 style='text-align: center;'> Recommendations </h3>", unsafe_allow_html=True)
                                colls = placeholder2.columns(5)
                                resultaaaa = recommend(film=movie_title)
                                m = 0
                                for id, nom in resultaaaa:    
                                    url = get_movie_poster_url(id)
                                    with colls[m]:
                                        m = m + 1
                                        st.image(url)
                                        st.write(nom)
                                st.session_state['clicked_index'] = -1
                    else:
                        with cols[j]:
                            clicked_index2 = clickable_images(
                                ['https://media.discordapp.net/attachments/845332355078029396/1208484578549956689/placeholder.jpeg?ex=65e373f8&is=65d0fef8&hm=ac08844340d87c8bd5cb39a0551367ef767f0328227f533c80956d90e360bc18&=&format=webp&width=446&height=671'],
                                titles=[movie_title],
                                div_style={"display": "flex", "justify-content": "center"},
                                img_style={"margin": "5px", "height": "200px"},
                            )
                            st.write(movie_title)
                            if clicked_index2 > -1:
                                placeholder.write(filmsynopsis)
                                resultaaaa = recommend(film=movie_title)
                                for id, nom in resultaaaa:    
                                        url = get_movie_poster_url(id)
                                        placeholder2.write(nom)
                                        if url != None:
                                            placeholder2.image(url)


def render_based_on_category(selected_category):
    if selected_category is not None:
        # Réinitialiser clicked_index à -1
        st.session_state['clicked_index'] = -1
        if selected_category == "Films":
            st.write("Cliquez sur un film pour avoir plus d'informations")
            tmdb_ids = df_filtered['tconst'].tolist()
            movie_titles = df_filtered['primaryTitle'].tolist()
            render_images(tmdb_ids, movie_titles, 50)
        elif selected_category == "Séries":
            st.write("Cliquez sur une série pour avoir plus d'informations")
            tmdb_ids = df_filtered['tconst'].tolist()
            movie_titles = df_filtered['primaryTitle'].tolist()
            render_images(tmdb_ids, movie_titles, 50)



# Appel de la fonction
render_based_on_category(selectedc) 