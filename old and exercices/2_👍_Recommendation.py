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

if 'selected_category' not in st.session_state:
    st.session_state['selected_category'] = None

if "selected_title" not in st.session_state:
    st.session_state['selected_title'] = None

# Initialisation de la BDD
engine = create_database_engine('BDD_URL.env')

# Dictionnaire de requêtes SQL
sql_requests = {
    "Films": "sqlrequests/SQLfilms.sql",
    "Série": "sqlrequests/SQLserie.sql",
    "FilmsX": "sqlrequests/SQLfilmsX.sql",
    "SérieX": "sqlrequests/SQLserieX.sql",
}

# Sidebar
st.sidebar.title("Catégorie")
# Ajouter une catégorie ici pour créer un nouveau bouton
categories = ["Films", "Série"]

explicit_warning = ''

for category in categories:
    if st.sidebar.button(category):
        st.session_state['selected_category'] = category
        if st.session_state.get("explicit_content", False):
            explicit_warning = "<p><font color='FF0000'> Attention, vous êtes soumis à du contenu sensible. </font> </p>"
            if category == "Films":
                with open('sqlrequests/SQLfilmsX.sql', 'r') as file:
                    SQL = file.read()
                    df = pd.read_sql(SQL, engine)
                    st.session_state['tmdb_ids'] = df['tconst']
                    st.session_state['movie_titles'] = df['primaryTitle']
                # st.write(df)
            elif category == "Série":
                with open('sqlrequests/SQLserieX.sql', 'r') as file:
                    SQL = file.read()
                    df = pd.read_sql(SQL, engine)
                    st.session_state['tmdb_ids'] = df['tconst']
                    st.session_state['movie_titles'] = df['primaryTitle']
                # st.write(df)
        else:
            explicit_warning = ""
            if category == "Films":
                with open('sqlrequests/SQLfilms.sql', 'r') as file:
                    SQL = file.read()
                    df = pd.read_sql(SQL, engine)
                    st.session_state['tmdb_ids'] = df['tconst']
                    st.session_state['movie_titles'] = df['primaryTitle']
                # st.write(df)
            elif category == "Série":
                with open('sqlrequests/SQLserie.sql', 'r') as file:
                    SQL = file.read()
                    df = pd.read_sql(SQL, engine)
                    st.session_state['tmdb_ids'] = df['tconst']
                    st.session_state['movie_titles'] = df['primaryTitle']
                # st.write(df)

# Informe la catégorie selectionnée            
if st.session_state['selected_category'] is not None:
    st.write(f"<p style='text-align:center;'> Vous êtes dans la catégorie '{st.session_state['selected_category']}' {explicit_warning}</p>", unsafe_allow_html=True)

# Checkbox pour afficher ou non le contenu explicite
checkboite = st.sidebar.checkbox("Contenu explicite", key="disabled")
st.session_state["explicit_content"] = checkboite

# Barre pour séparer le tout en markdown
st.markdown("---")
st.write("")

# Function de rendu d'images cliquables
def render_images(tmdb_ids, movie_titles, max_images):
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
                            clicked_index = clickable_images(
                                [poster_url],
                                titles=[movie_title],
                                div_style={"display": "flex", "justify-content": "center"},
                                img_style={"margin": "5px", "height": "200px"},
                            )
                            st.write(movie_title)
                            if clicked_index > -1:
                                st.write(filmsynopsis)
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
                                st.write(filmsynopsis)


# Basé sur la catégorie choisie avec des variables de session
def render_based_on_category(selected_category):
    if selected_category is not None:
        tmdb_ids = st.session_state.get('tmdb_ids')
        movie_titles = st.session_state.get('movie_titles')
        if tmdb_ids is not None and movie_titles is not None:
            if selected_category == "Films":
                st.write("Cliquez sur un film pour avoir plus d'informations")
                render_images(tmdb_ids, movie_titles, 250)
            elif selected_category == "Série":
                st.write("Cliquez sur une série pour avoir plus d'informations")
                render_images(tmdb_ids, movie_titles, 250)

render_based_on_category(st.session_state['selected_category'])

engine.dispose()