// app.js

const MovieApp = (() => {
    const fetchMovies = async (query = '', genre = '') => {
      const movieList = document.getElementById('movieList');
      try {
        const response = await fetch(`/movies?name=${query}&genre=${genre}`);
        const movies = await response.json();
  
        movieList.innerHTML = '';
  
        if (movies.length === 0) {
          movieList.innerHTML = '<li>Aucun film trouvé.</li>';
          return;
        }
  
        movies.forEach(movie => {
          const listItem = document.createElement('li');
          listItem.textContent = `${movie.name} (${movie.year}) - ${movie.genre} - Note : ${movie.rating}`;
          movieList.appendChild(listItem);
        });
      } catch (error) {
        console.error('Erreur lors de la récupération des films :', error);
        movieList.innerHTML = '<li>Échec du chargement des films. Veuillez réessayer plus tard.</li>';
      }
    };
  
    const initMovieApp = async () => {
      const searchInput = document.getElementById('searchInput');
      const searchButton = document.getElementById('searchButton');
      const genreSelect = document.getElementById('genreSelect');
      const filterButton = document.getElementById('filterButton');
  
      // Récupérer tous les films au chargement
      await fetchMovies();
  
      // Recherche
      searchButton.addEventListener('click', async () => {
        const query = searchInput.value.trim();
        await fetchMovies(query);
      });
  
      // Filtre par genre
      filterButton.addEventListener('click', async () => {
        const query = searchInput.value.trim();
        const selectedGenre = genreSelect.value;
        await fetchMovies(query, selectedGenre);
      });
    };
  
    // N'expose que initMovieApp
    return {
      initMovieApp,
    };
  })();
  





document.getElementById('execute').addEventListener('click', async () => {
    const query = document.getElementById('query').value;
    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query }),
        });
        const result = await response.json();
        document.getElementById('result').textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        document.getElementById('result').textContent = `Erreur : ${error.message}`;
    }
});

