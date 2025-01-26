from SPARQLWrapper import SPARQLWrapper, JSON
import os

# Fonction pour obtenir l'URL dynamique de Fuseki dans Codespaces
def get_fuseki_url(port=3030, dataset="dataset"):
    codespace_name = os.getenv("CODESPACE_NAME")
    if not codespace_name:
        raise EnvironmentError("CODESPACE_NAME variable not found. Make sure you are running this in a GitHub Codespace.")
    
    # Construire l'URL publique pour Codespaces
    region = "app.github.dev"  # Région correcte
    fuseki_url = f"https://{codespace_name}-{port}.{region}/{dataset}/sparql"
    return fuseki_url

# Obtenir l'URL dynamique
try:
    sparql_endpoint = get_fuseki_url(port=3030, dataset="Data_persistent_test")
    print(f"SPARQL endpoint: {sparql_endpoint}")
except Exception as e:
    print(f"Error while constructing SPARQL endpoint URL: {e}")
    exit(1)

# Initialiser SPARQLWrapper avec l'URL correcte
sparql = SPARQLWrapper(sparql_endpoint)

# Définir une requête SPARQL
query = """
    SELECT ?subject ?predicate ?object
    WHERE {
        ?subject ?predicate ?object.
    }
    LIMIT 10
"""

# Configurer SPARQLWrapper
sparql.setQuery(query)
sparql.setReturnFormat(JSON)

# Exécuter et afficher les résultats avec gestion des erreurs
try:
    # Lire la réponse brute
    response = sparql.query().response.read()
    print("Raw response:", response)  # Affiche la réponse brute pour déboguer

    # Convertir en JSON
    results = sparql.query().convert()
    if "results" in results and "bindings" in results["results"]:
        for result in results["results"]["bindings"]:
            subject = result.get('subject', {}).get('value', 'N/A')
            predicate = result.get('predicate', {}).get('value', 'N/A')
            object_ = result.get('object', {}).get('value', 'N/A')
            print(f"Subject: {subject}, Predicate: {predicate}, Object: {object_}")
    else:
        print("No results found or incorrect format returned.")
except Exception as e:
    print(f"Error while querying SPARQL endpoint: {e}")