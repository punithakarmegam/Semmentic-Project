/*to interact with fuseki
async function querySPARQL() {
  const genre = document.getElementById('genre').value;
  const endpoint = 'http://localhost:3030/dataset/sparql';

  const query = `
    PREFIX : <http://example.org/entertainment#>
    SELECT ?movie WHERE {
      ?movie a :Movie ;
             :hasGenre "${genre}" .
    }
  `;

  const response = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ query }),
  });

  const data = await response.json();
  const results = data.results.bindings.map(b => b.movie.value);

  const resultsList = document.getElementById('results');
  resultsList.innerHTML = results.map(movie => `<li>${movie}</li>`).join('');
}*/

// Affiche les résultats de recherche
function displayResults(results) {
  const resultsList = document.getElementById("resultsList");
  resultsList.innerHTML = "";

  if (results.length === 0) {
    resultsList.innerHTML = "<li>No results found</li>";
    return;
  }

  results.forEach((result) => {
    const li = document.createElement("li");
    li.textContent = result;
    resultsList.appendChild(li);
  });
}

// Requête SPARQL vers Fuseki
/*async function querySPARQL() {
  const genre = document.getElementById('genre').value;  
  //const endpoint = 'http://localhost:3030/entertainment/sparql';
  const endpoint = 'http://localhost:5000/proxy';


  const query = `
  PREFIX schema: <http://schema.org/>
  SELECT ?name ?genre ?year WHERE {
      ?movie a schema:Movie ;
             schema:name ?name ;
             schema:genre ?genre ;
             schema:datePublished ?year .
      FILTER(CONTAINS(LCASE(?genre), "${genre.toLowerCase()}"))
  } LIMIT 10`;

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      mode: 'cors',  // ✅ Ajoute ceci pour éviter les erreurs CORS
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
      },
      body: new URLSearchParams({ query })
    });

    if (!response.ok) {
      throw new Error("Erreur lors de la requête SPARQL.");
    }

    const data = await response.json();
    const resultsList = document.getElementById('resultsList');
    resultsList.innerHTML = "";

    if (data.results.bindings.length > 0) {
      data.results.bindings.forEach(movie => {
        const li = document.createElement('li');
        li.textContent = `${movie.name.value} - ${movie.genre.value} (${movie.year.value})`;
        resultsList.appendChild(li);
      });
    } else {
      resultsList.innerHTML = "<li>Aucun résultat trouvé</li>";
    }

  } catch (error) {
    console.error("Erreur lors de la requête SPARQL :", error);
    document.getElementById('resultsList').innerHTML = "<li>Erreur de connexion à Fuseki</li>";
  }
}*/
async function querySPARQL() {
  const genre = document.getElementById('genre').value;  
  const endpoint = 'http://localhost:5000/proxy';  // Changer pour le proxy Flask a supp 

  const query = `
  PREFIX schema: <http://schema.org/>
  SELECT ?name ?genre ?year WHERE {
      ?movie a schema:Movie ;
             schema:name ?name ;
             schema:genre ?genre ;
             schema:datePublished ?year .
      FILTER(CONTAINS(LCASE(?genre), "${genre.toLowerCase()}"))
  } LIMIT 10`;

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
      },
      body: new URLSearchParams({ query })
    });

    if (!response.ok) {
      throw new Error("Erreur lors de la requête SPARQL.");
    }

    const data = await response.json();
    const resultsList = document.getElementById('resultsList');
    resultsList.innerHTML = "";

    if (data.results.bindings.length > 0) {
      data.results.bindings.forEach(movie => {
        const li = document.createElement('li');
        li.textContent = `${movie.name.value} - ${movie.genre.value} (${movie.year.value})`;
        resultsList.appendChild(li);
      });
    } else {
      resultsList.innerHTML = "<li>Aucun résultat trouvé</li>";
    }

  } catch (error) {
    console.error("Erreur lors de la requête SPARQL :", error);
    document.getElementById('resultsList').innerHTML = "<li>Erreur de connexion au serveur</li>";
  }
}


// Lien avec le bouton de recherche
document.getElementById("searchButton").addEventListener("click", querySPARQL);


