from stimports import *

# Initialisation des valeurs session

if "explicit_content" not in st.session_state:
    st.session_state["explicit_content"] = False

if 'selected_category' not in st.session_state:
    st.session_state['selected_category'] = None


# Initialisation de la BDD
engine = create_database_engine('BDD_URL.env')


# Ecran titre avec logo
image = "ressources/title.png"
st.image(image, caption=None, width=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
st.markdown("<h2 style='text-align: center;'>On regarde quoi ce soir ?</h2>", unsafe_allow_html=True)
st.write("")

# Sidebar
st.sidebar.title("Catégorie")

# Ajouter une catégorie ici pour créer un nouveau bouton
categories = ["Films", "Série"]
for category in categories:
    if st.sidebar.button(category):
        st.session_state['selected_category'] = category
        if category == "Films":
                with open('sqlrequests/SQLfilms.sql', 'r') as file:
                    SQL = file.read()
                    df = pd.read_sql(SQL, engine)
                st.write(df)
        if category == "Série":
                with open('sqlrequests/SQLserie.sql','r') as file:
                    SQL = file.read()
                    df = pd.read_sql(SQL, engine)
                st.write(df)

if st.session_state['selected_category'] is not None:
    st.write(f"<p style='text-align:center;'> Vous êtes dans la catégorie '{st.session_state['selected_category']}'</p>", unsafe_allow_html=True)

checkboite = st.sidebar.checkbox("Contenu explicite", key="disabled")
st.session_state["explicit_content"] = checkboite
st.sidebar.write(st.session_state["explicit_content"])

st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')


if st.sidebar.button("Relâcher connexion SQL") :
    engine.dispose()


# Barre de recherche
search_query = st.text_input('Rechercher :')
if st.button("Rechercher"):
    if st.session_state['selected_category'] is None:
        st.error("Veuillez sélectionner une catégorie avant de lancer la recherche.")
    else:
        # Exemple de requête SQL
        st.write(SQL_director_crewnames)
        st.session_state['selected_category'] = None

st.markdown("---")
st.write("")


tmdb_ids = df['tconst']
for i in range(0, len(tmdb_ids), 4):
    cols = st.columns(4)
    for j in range(4):
        index = i + j
        if index < len(tmdb_ids):
            tmdb_id = tmdb_ids[index]
            poster_url = get_movie_poster_url(tmdb_id)
            if poster_url:
                with cols[j]:
                    st.image(poster_url, use_column_width=True, caption=tmdb_id)
            else:
                with cols[j]:
                    st.image('ressources/placeholder.jpg')