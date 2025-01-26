import kagglehub
import pandas as pd
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD, FOAF
import os
from datetime import datetime
import requests

# Télécharge dataset IMDb
path = kagglehub.dataset_download("harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows")
file_path = os.path.join(path, "imdb_top_1000.csv")

# Charge et nettoie les données
data = pd.read_csv(file_path)

# Affiche les colonnes disponibles pour vérification
print("Colonnes disponibles : ", data.columns)

# Nettoyage des données (supprime les lignes avec des valeurs manquantes)
movies_cleaned = data.dropna()

# Renommer pour normalisation
movies_cleaned = movies_cleaned.rename(columns={
    'Series_Title': 'Title',
    'Released_Year': 'Year'
})

# Assure que l'année est numérique
movies_cleaned = movies_cleaned[movies_cleaned['Year'].str.isnumeric()]
movies_cleaned['Year'] = movies_cleaned['Year'].astype(int)

# Sauvegarde données nettoyées
movies_cleaned.to_csv("cleaned_movies.csv", index=False)
print("Données nettoyées sauvegardées dans cleaned_movies.csv")

# Création du graphe RDF
EX = Namespace("http://example.org/")
SCHEMA = Namespace("http://schema.org/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

g = Graph()
g.bind("ex", EX)
g.bind("schema", SCHEMA)
g.bind("foaf", FOAF)

# Conversion données en RDF
for index, row in movies_cleaned.iterrows():
    movie_uri = EX[f"Movie_{index}"]

    # Ajouter info de base
    g.add((movie_uri, RDF.type, SCHEMA.Movie))
    g.add((movie_uri, SCHEMA.name, Literal(row['Title'], datatype=XSD.string)))
    g.add((movie_uri, SCHEMA.genre, Literal(row['Genre'], datatype=XSD.string)))
    g.add((movie_uri, SCHEMA.datePublished, Literal(str(row['Year']), datatype=XSD.gYear)))
    g.add((movie_uri, SCHEMA.runtime, Literal(row['Runtime'], datatype=XSD.string)))
    g.add((movie_uri, SCHEMA.contentRating, Literal(row['Certificate'], datatype=XSD.string)))
    g.add((movie_uri, SCHEMA.ratingValue, Literal(str(row['IMDB_Rating']), datatype=XSD.float)))
    g.add((movie_uri, SCHEMA.description, Literal(row['Overview'], datatype=XSD.string)))

    # Ajouter colonnes supplémentaires 
    if 'Meta_score' in row and pd.notna(row['Meta_score']):
        g.add((movie_uri, SCHEMA.aggregateRating, Literal(row['Meta_score'], datatype=XSD.integer)))

    if 'No_of_votes' in row and pd.notna(row['No_of_votes']):
        g.add((movie_uri, SCHEMA.votes, Literal(row['No_of_votes'], datatype=XSD.integer)))

    if 'Gross' in row and pd.notna(row['Gross']):
        g.add((movie_uri, SCHEMA.grossRevenue, Literal(row['Gross'], datatype=XSD.string)))

    # Ajout réalisateurs
    director_uri = EX[f"Director_{row['Director'].replace(' ', '_')}"]
    g.add((director_uri, RDF.type, FOAF.Person))
    g.add((director_uri, FOAF.name, Literal(row['Director'], datatype=XSD.string)))
    g.add((movie_uri, SCHEMA.director, director_uri))

    # Ajout acteurs principaux
    for i in range(1, 5):  
        star_col = f'Star{i}'
        if star_col in row and pd.notna(row[star_col]):
            star_uri = EX[f"Actor_{row[star_col].replace(' ', '_')}"]
            g.add((star_uri, RDF.type, FOAF.Person))
            g.add((star_uri, FOAF.name, Literal(row[star_col], datatype=XSD.string)))
            g.add((movie_uri, SCHEMA.actor, star_uri))

# Sauvegarde Turtle
output_file = f"movies_{datetime.now().strftime('%Y-%m-%d')}.ttl"
g.serialize(destination=output_file, format="turtle")
print(f"RDF exporté avec succès : {output_file}")

# --- Upload Automatique vers Fuseki ---
FUSEKI_URL = "http://localhost:3030"
DATASET_NAME = "entertainment"
UPLOAD_ENDPOINT = f"{FUSEKI_URL}/{DATASET_NAME}/data"

# Crée automatiquement dataset s'il n'existe pas
def create_dataset():
    dataset_endpoint = f"{FUSEKI_URL}/$/datasets"
    response = requests.post(
        dataset_endpoint,
        data={"dbName": DATASET_NAME, "dbType": "tdb"},
    )
    if response.status_code == 200 or response.status_code == 409:
        print(f"Dataset '{DATASET_NAME}' prêt.")
    else:
        raise Exception(f"Erreur création dataset : {response.text}")

# Envoie fichier TTL vers Fuseki
def upload_ttl(file_path):
    with open(file_path, 'rb') as f:
        response = requests.post(
            UPLOAD_ENDPOINT,
            headers={"Content-Type": "text/turtle"},
            data=f
        )
    if response.status_code == 200:
        print(f"{file_path} chargé avec succès dans Fuseki.")
    else:
        print(f"Erreur lors du chargement : {response.text}")

if __name__ == "__main__":
    try:
        create_dataset()
        upload_ttl(output_file)
    except Exception as e:
        print(f"Erreur : {e}")
