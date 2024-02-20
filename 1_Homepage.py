from ressources.stimports import *

# Onglet de la page
st.set_page_config(
        page_title= "Netfloox - Home",
        page_icon= "🍿"
)

image = "ressources/title.png"
st.image(image, caption=None, width=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
st.write("")
st.markdown("---")
st.markdown("<h2 style='text-align: center; color: white;'>Projet réalisé par :</h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>Pierre Cavallo</h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>Mohammed Haouach</h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>Clément NOGUES</h2>", unsafe_allow_html=True)