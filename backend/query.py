#for sparql requestion
from SPARQLWrapper import SPARQLWrapper, JSON

SPARQL_ENDPOINT = "http://localhost:3030/dataset/sparql"

def get_recommendations(genre):
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setQuery(f"""
        PREFIX : <http://example.org/entertainment#>
        SELECT ?movie WHERE {{
          ?movie a :Movie ;
                 :hasGenre "{genre}" .
        }}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    recommendations = [result['movie']['value'] for result in results['results']['bindings']]
    return recommendations

# Exemple d'utilisation
genre = "Sci-Fi"
movies = get_recommendations(genre)
print(f"Movies for genre '{genre}': {movies}")
