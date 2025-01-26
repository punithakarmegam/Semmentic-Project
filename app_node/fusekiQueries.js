const axios = require('axios');

const FUSEKI_ENDPOINT = 'http://localhost:3030/entertainment';

// Fonction pour récupérer films depuis Fuseki
async function getMovies() {
    const sparqlQuery = `
    PREFIX schema: <http://schema.org/>
    SELECT ?name ?genre ?year ?rating
    WHERE {
        ?movie a schema:Movie ;
               schema:name ?name ;
               schema:genre ?genre ;
               schema:datePublished ?year ;
               schema:ratingValue ?rating .
    }
    LIMIT 1000
    `; 

    try {
        console.log("Envoi de la requête SPARQL à Fuseki...");

        const response = await axios.post(
            `${FUSEKI_ENDPOINT}/query`,
            sparqlQuery,
            {
                headers: { 'Content-Type': 'application/sparql-query' }, // Headers obligatoires pour SPARQL
            }
        );

        console.log("Réponse obtenue :", JSON.stringify(response.data, null, 2));

        // Vérification structure de réponse
        if (!response.data.results || !response.data.results.bindings) {
            throw new Error('La réponse de Fuseki ne contient pas les résultats attendus.');
        }

        // Formater résultats pour site
        return response.data.results.bindings.map((binding) => ({
            name: binding.name?.value || 'Inconnu', // Utilisation de valeurs par défaut en cas d'absence
            genre: binding.genre?.value || 'Non spécifié',
            year: binding.year?.value || 'Inconnue',
            rating: binding.rating?.value || 'Non noté',
        }));
    } catch (error) {
        console.error('Erreur lors de l\'exécution de la requête SPARQL :', error.response?.data || error.message);
        throw new Error('Erreur lors de l\'exécution de la requête SPARQL.');
    }
}

module.exports = { getMovies };
