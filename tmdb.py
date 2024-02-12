import os
import requests

# Dossier de destination pour enregistrer les jaquettes
destination_folder = "jaquettes"

# Fonction pour récupérer l'URL de la jaquette d'un film à partir de TMDb
def get_movie_poster_url(tmdb_id):
    api_key = '330f02856761de4af7dcfbad30b193ae'
    base_url = 'https://api.themoviedb.org/3/movie/'
    endpoint = f'{tmdb_id}?api_key={api_key}'
    response = requests.get(base_url + endpoint)
    if response.status_code == 200:
        data = response.json()
        if 'poster_path' in data:
            poster_path = data['poster_path']
            return f'https://image.tmdb.org/t/p/w500/{poster_path}'
    return None

# Fonction pour enregistrer la jaquette localement
def save_movie_poster_locally(tmdb_id, destination_folder):
    poster_url = get_movie_poster_url(tmdb_id)
    if poster_url:
        # Télécharger l'image
        response = requests.get(poster_url)
        if response.status_code == 200:
            # Créer le dossier de destination s'il n'existe pas
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            # Enregistrer l'image localement
            with open(os.path.join(destination_folder, f'{tmdb_id}.jpg'), 'wb') as f:
                f.write(response.content)
            print('Jaquette enregistrée avec succès.')
            return os.path.join(destination_folder, f'{tmdb_id}.jpg')
    print('Impossible de récupérer la jaquette du film.')
    return None

# Exemple d'utilisation
tmdb_id = 'tt0069189'
jaquette_path = save_movie_poster_locally(tmdb_id, destination_folder)
if jaquette_path:
    print('Jaquette enregistrée localement:', jaquette_path)
else:
    print('Impossible de récupérer la jaquette du film.')