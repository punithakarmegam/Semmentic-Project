#charger données RDF dans fuseki
import requests
import os

FUSEKI_URL = "http://localhost:3030"
DATASET_NAME = "entertainment"
UPLOAD_ENDPOINT = f"{FUSEKI_URL}/{DATASET_NAME}/data"
dir = os.chdir('/workspaces/Web_Semantics_project/backend/') 

# Trouver le fichier TTL le plus récent
def find_latest_ttl_file(content_file):
    files = os.listdir()
    print("Fichiers détectés :", files)

    if content_file == "movies":

        files = os.listdir()
        print("Fichiers détectés :", files)
        ttl_files = [f for f in files if f.startswith('movies_') and f.endswith('.ttl')]
        if not ttl_files:
            raise FileNotFoundError("Aucun fichier .ttl trouvé")
        print('fichier movies trouvé')
        latest_file = max(ttl_files, key=os.path.getctime)
        return latest_file

    if content_file == "games":
            
        ttl_files = [f for f in files if f.startswith('games_') and f.endswith('.ttl')]
        if not ttl_files:
            raise FileNotFoundError("Aucun fichier .ttl trouvé")
        print('fichier games trouvé')
        latest_file = max(ttl_files, key=os.path.getctime)
        return latest_file

# Créer dataset s'il n'existe pas
def create_dataset():
    response = requests.post(
        f"{FUSEKI_URL}/$/datasets",
        data={"dbName": DATASET_NAME, "dbType": "tdb"}
    )
    if response.status_code in [200, 409]:
        print(f"Dataset '{DATASET_NAME}' prêt.")
    else:
        raise Exception("Erreur lors de la création du dataset")

# Upload automatique du fichier TTL
def upload_ttl(file_path):
    with open(file_path, 'rb') as f:
        response = requests.post(
            UPLOAD_ENDPOINT,
            headers={"Content-Type": "text/turtle"},
            data=f
        )
    if response.status_code == 200:
        print(f"{file_path} chargé avec succès.")
    else:
        print(f"Erreur : {response.text}")

if __name__ == "__main__":
    try:
        create_dataset()
        latest_ttl = find_latest_ttl_file("movies")
        latest_game = find_latest_ttl_file("games")

        upload_ttl(latest_ttl)
        upload_ttl(latest_game)
    except Exception as e:
        print(f"Erreur : {e}")
