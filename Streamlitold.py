import streamlit as st
import os

image = "ressources\\titre.png"

# Titre
st.image(image, caption=None, width=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
st.markdown("<h2 style='text-align: center;'>On regarde quoi ce soir ?</h2>", unsafe_allow_html=True)
st.write("")

# Sidebar
st.sidebar.title("Sidebar")

 # ajouter un truc a la liste pour ajouter un bouton
options = ["Films", "Série", "18+"]

for option in options:
    if st.sidebar.button(option):
        st.write(f"<p style='text-align:center;'> Vous êtes dans la catégorie '{option}'</p>", unsafe_allow_html=True)

search_query = st.text_input('Rechercher :')

st.markdown("---")
st.write("")


image_folder = "jaquettes"

image_files = os.listdir(image_folder)


num_columns = 3

# Afficher les images en utilisant une grille
for i in range(0, len(image_files), num_columns):
    # Créer une nouvelle rangée dans la grille
    col1, col2, col3 = st.columns(num_columns)
    for j in range(num_columns):
        index = i + j
        if index < len(image_files):
            # Afficher l'image correspondante dans la colonne
            with col1, col2:
                st.image(os.path.join(image_folder, image_files[index]), use_column_width=False, caption=image_files[index])