import requests
import json
from time import sleep
import pandas as pd
from rdflib import Graph, Literal, Namespace, RDF, XSD
import pandas as pd
import zipfile
import os

# Charger les fichiers JSON depuis le fichier ZIP
with zipfile.ZipFile("games_igdb_all_data.zip", 'r') as z:
    # Lire chaque fichier JSON dans une DataFrame
    with z.open("games_igdb_all_data.json") as f:
        data_game = pd.read_json(f)

# Afficher les DataFrames pour vérifier
print(data_game.head())

# Charger les fichiers JSON depuis le fichier ZIP
with zipfile.ZipFile("games_igdb_cover.zip", 'r') as z:
    # Lire chaque fichier JSON dans une DataFrame
    with z.open("games_igdb_cover.json") as f:
        data_cover = pd.read_json(f)

# Afficher les DataFrames pour vérifier
print(data_cover.head())

# Charger les fichiers JSON depuis le fichier ZIP
with zipfile.ZipFile("games_igdb_genre.zip", 'r') as z:
    # Lire chaque fichier JSON dans une DataFrame
    with z.open("games_igdb_genre.json") as f:
        data_genre = pd.read_json(f)

# Afficher les DataFrames pour vérifier
print(data_genre.head())

# Charger les fichiers JSON depuis le fichier ZIP
with zipfile.ZipFile("games_igdb_platform.zip", 'r') as z:
    # Lire chaque fichier JSON dans une DataFrame
    with z.open("games_igdb_platform.json") as f:
        data_platform = pd.read_json(f)

# Afficher les DataFrames pour vérifier
print(data_platform.head())

# Transformation des données pour faciliter le remplacement
covers_dict = data_cover.set_index("id")["url"].to_dict()
genres_dict = data_genre.set_index("id")["name"].to_dict()
platforms_dict = data_platform.set_index("id")["name"].to_dict()

# Fonction pour enrichir un jeu
def enrich_game(game):
    # Ajouter la couverture si disponible
    game["cover_url"] = covers_dict.get(game.get("cover"), "Unknown Cover")
    
    # Supprimer les deux premiers "//" dans l'URL
    if isinstance(game["cover_url"], str):  # Vérifie si cover_url est une chaîne
        game["cover_url"] = game["cover_url"].replace("//", "", 1)
    
    # Ajouter les genres si disponibles
    genres = game.get("genres", [])
    if not isinstance(genres, list):  # Vérifie si genres est une liste
        genres = []
    game["genres_names"] = [genres_dict.get(gid, "Unknown Genre") for gid in genres]
    
    # Ajouter les plateformes si disponibles
    platforms = game.get("platforms", [])
    if not isinstance(platforms, list):  # Vérifie si platforms est une liste
        platforms = []
    game["platforms_names"] = [platforms_dict.get(pid, "Unknown Platform") for pid in platforms]
    
    return game

# Appliquer l'enrichissement
enriched_games = data_game.apply(lambda row: enrich_game(row), axis=1)

# Sauvegarder dans un nouveau fichier JSON
enriched_games.to_json("enriched_games.json", orient="records", indent=4)

print("Le fichier JSON enrichi a été créé avec succès !")

data_games_cleaned = pd.read_json("enriched_games.json")
data_games_cleaned = data_games_cleaned.dropna()

# Renommer pour normalisation
data_games_cleaned = data_games_cleaned.rename(columns={
    'name': 'Title',
    'first_release_date': 'Release Date'
})

data_games_cleaned['Release Date'] = pd.to_datetime(data_games_cleaned['Release Date'], unit='s').dt.strftime('%Y-%m-%d')
data_games_cleaned = data_games_cleaned.drop(columns=["genres", "platforms","cover"])

# Sauvegarder dans un nouveau fichier JSON
data_games_cleaned.to_json("data_games_cleaned.json", orient="records", indent=4)

print("Le fichier JSON enrichi a été créé avec succès !")

# Nettoyage des barres obliques inversées dans le fichier JSON
with open("data_games_cleaned.json", "r", encoding="utf-8") as file:
    content = file.read()

# Supprime les backslashes
clean_content = content.replace("\\/", "/")

# Sauvegarde dans le même fichier
with open("data_games_cleaned.json", "w", encoding="utf-8") as file:
    file.write(clean_content)

os.remove("enriched_games.json")
print("Le fichier JSON a été suprimé avec succès !")

# Sauvegarder les résultats dans un fichier JSON temporaire
temp_json_file = "data_games_cleaned.json"
output_zip = "data_games_cleaned.zip"

# Ajouter le fichier JSON dans un fichier ZIP
with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(temp_json_file, os.path.basename(temp_json_file))

# Supprimer le fichier JSON temporaire
os.remove(temp_json_file)

print(f"Tous les jeux ont été sauvegardés dans {output_zip}.")


# Charger les données des jeux vidéo
with zipfile.ZipFile("data_games_cleaned.zip", 'r') as z:
    # Lire chaque fichier JSON dans une DataFrame
    with z.open("data_games_cleaned.json") as f:
        data = pd.read_json(f)

# Création des namespaces
EX = Namespace("http://example.org/game/")
SCHEMA = Namespace("http://schema.org/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

# Création du graphe RDF
g = Graph()
g.bind("ex", EX)
g.bind("schema", SCHEMA)
g.bind("foaf", FOAF)

# Conversion des données en RDF
for index, row in data.iterrows():
    if index < len(data)/5 :

        game_uri = EX[f"Game_{row['id']}"]

        # Ajouter les informations de base
        g.add((game_uri, RDF.type, SCHEMA.VideoGame))
        g.add((game_uri, SCHEMA.name, Literal(row['Title'], datatype=XSD.string)))
        g.add((game_uri, SCHEMA.datePublished, Literal(row['Release Date'], datatype=XSD.date)))
        g.add((game_uri, SCHEMA.description, Literal(f"Category: {row['category']}", datatype=XSD.string)))
        g.add((game_uri, SCHEMA.image, Literal(row['cover_url'], datatype=XSD.anyURI)))

        # Ajouter les genres
        if isinstance(row['genres_names'], list):
            for genre in row['genres_names']:
                g.add((game_uri, SCHEMA.genre, Literal(genre, datatype=XSD.string)))

        # Ajouter les plateformes
        if isinstance(row['platforms_names'], list):
            for platform in row['platforms_names']:
                g.add((game_uri, SCHEMA.gamePlatform, Literal(platform, datatype=XSD.string)))


# Sauvegarder au format Turtle
output_file = f"games_{pd.Timestamp.now().strftime('%Y-%m-%d')}.ttl"
g.serialize(destination=output_file, format="turtle")
print(f"RDF exporté avec succès : {output_file}")

