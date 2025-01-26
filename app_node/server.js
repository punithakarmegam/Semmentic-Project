const express = require('express');
const { getMovies } = require('./fusekiQueries');
const bodyParser = require('body-parser');
const axios = require('axios');
const path = require('path');

const app = express();
const FUSEKI_ENDPOINT = 'http://localhost:3030/entertainment'; // Remplacez par l'URL de votre instance Fuseki

// Middleware pour parser les requêtes JSON
app.use(bodyParser.json());

// Servir les fichiers statiques du dossier 'public'
app.use(express.static(path.join(__dirname, 'public')));

// Endpoint pour tester le serveur
app.get('/', (req, res) => {
    // Servir le fichier index.html par défaut
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Endpoint pour exécuter une requête SPARQL
app.post('/query', async (req, res) => {
    const sparqlQuery = req.body.query;
    if (!sparqlQuery) {
        return res.status(400).json({ error: 'La requête SPARQL est manquante.' });
    }
    try {
        const response = await axios.post(
            `${FUSEKI_ENDPOINT}/sparql`, // Corrigé avec des backticks
            sparqlQuery,
            {
                headers: { 'Content-Type': 'application/sparql-query' },
            }
        );
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: `Erreur lors de la requête : ${error.message}` }); // Corrigé avec des backticks
    }
});

// Lancer le serveur
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Serveur en cours d'exécution sur http://localhost:${PORT}`); // Corrigé avec des backticks
});

// Endpoint pour récupérer films
app.get('/movies', async (req, res) => {
    try {
      const { name, genre } = req.query;

      // Récupérer tous films
      let movies = await getMovies();

      // Filtrer par nom
      if (name) {
        const lowerCaseName = name.toLowerCase();
        movies = movies.filter(movie => movie.name.toLowerCase().includes(lowerCaseName));
      }

      // Filtrer par genre
      if (genre) {
        movies = movies.filter(movie => movie.genre.includes(genre));
      }

      res.json(movies);
    } catch (error) {
      console.error(error.message);
      res.status(500).json({ error: 'Error fetching movies.' });
    }
});
