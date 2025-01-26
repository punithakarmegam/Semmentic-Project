#!/bin/bash
GENRE="Sci-Fi"
curl -X POST \
     --data-urlencode "query=PREFIX : <http://example.org/entertainment#>
     SELECT ?movie WHERE {
       ?movie a :Movie ;
              :hasGenre \"$GENRE\" .
     }" \
     http://localhost:3030/dataset/sparql
