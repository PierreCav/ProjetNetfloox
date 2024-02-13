from stimports import *

# Session state valeur pour catégories
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
categories = ["Films", "Série", "18+"]
for category in categories:
    if st.sidebar.button(category):
        st.session_state['selected_category'] = category
        st.write(f"<p style='text-align:center;'> Vous êtes dans la catégorie '{category}'</p>", unsafe_allow_html=True)

sqklskdj = 'SET search_path to principal; SELECT * from "filmview" where "runtimeMinutes" Is NOT null and "titleType" = "movie" limit 10000;'


if st.sidebar.button("Engine Dispose") :
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


image_folder = "jaquette"

image_files = os.listdir(image_folder)


num_columns = 4

for i in range(0, len(image_files), num_columns):
    cols = st.columns(num_columns)
    for j in range(num_columns):
        index = i + j
        if index < len(image_files):
            with cols[j]:
                st.image(os.path.join(image_folder, image_files[index]), use_column_width=True)