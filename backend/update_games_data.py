import requests
import json
from time import sleep
import pandas as pd
from rdflib import Graph, Literal, Namespace, RDF, XSD
import pandas as pd
import zipfile
import os

# Vos identifiants IGDB
CLIENT_ID = "bvsy8b4wjxd3rrq91awg8dtlyqvcob"
CLIENT_SECRET = "rylgg35wx4ixwh6p48vte0z41s7p4y"

# URL pour obtenir le token d'accès
TOKEN_URL = "https://id.twitch.tv/oauth2/token"
API_URL = "https://api.igdb.com/v4/"

def get_access_token(client_id, client_secret):
    """Obtenir un jeton d'accès pour l'API IGDB."""
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(TOKEN_URL, params=params)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Erreur lors de la récupération du token : {response.status_code}, {response.text}")
def get_access_token(client_id, client_secret):
    """Obtenir un jeton d'accès pour l'API IGDB."""
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(TOKEN_URL, params=params)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Erreur lors de la récupération du token : {response.status_code}, {response.text}")

access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
print("Jeton d'accès récupéré avec succès.")

def fetch_all_games(api_url, access_token, client_id, output_zip):
    """Récupérer tous les jeux de la base de données IGDB."""
    api_url += "games"
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}',
    }
    games = []
    offset = 0
    limit = 500  # Limite maximale autorisée par requête
    while True:
        data = (
            f"fields name, first_release_date, category, cover, genres, name, platforms"
            # f"collection,language_supports,multiplayer_modes,dlcs,created_at"
            f"; limit {limit}; offset {offset};"
        )
        response = requests.post(api_url, headers=headers, data=data)
        if response.status_code == 200:
            batch = response.json()
            if not batch:
                break  # Fin des résultats
            games.extend(batch)
            offset += limit
            print(f"Récupéré {len(batch)} jeux, offset actuel : {offset}")
            sleep(0.1)  # Éviter de surcharger l'API
        else:
            raise Exception(f"Erreur lors de la requête : {response.status_code}, {response.text}")

    # Sauvegarder les résultats dans un fichier JSON temporaire
    temp_json_file = "games_igdb_all_data.json"
    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump(games, f, ensure_ascii=False, indent=4)

    # Ajouter le fichier JSON dans un fichier ZIP
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(temp_json_file, os.path.basename(temp_json_file))

    # Supprimer le fichier JSON temporaire
    os.remove(temp_json_file)

    print(f"Tous les jeux ont été sauvegardés dans {output_zip}.")

def fetch_covers(api_url, access_token, client_id, output_zip):
    api_url += "covers"
    """Récupérer tous les cover de jeux de la base de données IGDB."""
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}',
    }
    covers = []
    offset = 0
    limit = 500  # Limite maximale autorisée par requête
    while True:
        data = (
            f"fields image_id, url"
            f"; limit {limit}; offset {offset};"
        )
        response = requests.post(api_url, headers=headers, data=data)
        if response.status_code == 200:
            batch = response.json()
            if not batch:
                break  # Fin des résultats
            covers.extend(batch)
            offset += limit
            print(f"Récupéré {len(batch)} jeux, offset actuel : {offset}")
            sleep(0.1)  # Éviter de surcharger l'API
        else:
            raise Exception(f"Erreur lors de la requête : {response.status_code}, {response.text}")
            
    # Sauvegarder les résultats dans un fichier JSON temporaire
    temp_json_file = "games_igdb_cover.json"
    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump(covers, f, ensure_ascii=False, indent=4)

    # Ajouter le fichier JSON dans un fichier ZIP
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(temp_json_file, os.path.basename(temp_json_file))

    # Supprimer le fichier JSON temporaire
    os.remove(temp_json_file)

    print(f"Tous les jeux ont été sauvegardés dans {output_zip}.")

def fetch_genres(api_url, access_token, client_id, output_zip):
    api_url += "genres"
    """Récupérer tous les cover de jeux de la base de données IGDB."""
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}',
    }
    genres = []
    offset = 0
    limit = 500  # Limite maximale autorisée par requête
    while True:
        data = (
            f"fields name,slug"
            f"; limit {limit}; offset {offset};"
        )
        response = requests.post(api_url, headers=headers, data=data)
        if response.status_code == 200:
            batch = response.json()
            if not batch:
                break  # Fin des résultats
            genres.extend(batch)
            offset += limit
            print(f"Récupéré {len(batch)} jeux, offset actuel : {offset}")
            sleep(0.5)  # Éviter de surcharger l'API
        else:
            raise Exception(f"Erreur lors de la requête : {response.status_code}, {response.text}")

    # Sauvegarder les résultats dans un fichier JSON temporaire
    temp_json_file = "games_igdb_genre.json"
    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump(genres, f, ensure_ascii=False, indent=4)

    # Ajouter le fichier JSON dans un fichier ZIP
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(temp_json_file, os.path.basename(temp_json_file))

    # Supprimer le fichier JSON temporaire
    os.remove(temp_json_file)

    print(f"Tous les jeux ont été sauvegardés dans {output_zip}.")

def fetch_platforms(api_url, access_token, client_id, output_zip):
    api_url += "platforms"
    """Récupérer tous les cover de jeux de la base de données IGDB."""
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}',
    }
    platforms = []
    offset = 0
    limit = 500  # Limite maximale autorisée par requête
    while True:
        data = (
            f"fields abbreviation,alternative_name,generation,name,slug"
            f"; limit {limit}; offset {offset};"
        )
        response = requests.post(api_url, headers=headers, data=data)
        if response.status_code == 200:
            batch = response.json()
            if not batch:
                break  # Fin des résultats
            platforms.extend(batch)
            offset += limit
            print(f"Récupéré {len(batch)} jeux, offset actuel : {offset}")
            sleep(0.5)  # Éviter de surcharger l'API
        else:
            raise Exception(f"Erreur lors de la requête : {response.status_code}, {response.text}")

    # Sauvegarder les résultats dans un fichier JSON temporaire
    temp_json_file = "games_igdb_platform.json"
    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump(platforms, f, ensure_ascii=False, indent=4)

    # Ajouter le fichier JSON dans un fichier ZIP
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(temp_json_file, os.path.basename(temp_json_file))

    # Supprimer le fichier JSON temporaire
    os.remove(temp_json_file)

    print(f"Tous les jeux ont été sauvegardés dans {output_zip}.")

# Récupérer tous les jeux
fetch_all_games(API_URL, access_token, CLIENT_ID,"games_igdb_all_data.zip")
fetch_covers(API_URL, access_token, CLIENT_ID,"games_igdb_cover.zip")
fetch_genres(API_URL, access_token, CLIENT_ID,"games_igdb_genre.zip")
fetch_platforms(API_URL, access_token, CLIENT_ID,"games_igdb_platform.zip")
