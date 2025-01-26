const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('http://localhost:5000/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('username', username);
                window.location.href = 'index.html';
            } else {
                alert(data.message || 'Erreur de connexion');
            }
        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur lors de la connexion');
        }
    });
}

const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        if (password !== confirmPassword) {
            alert('Les mots de passe ne correspondent pas');
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            });

            const data = await response.json();

            if (response.ok) {
                alert('Inscription réussie! Vous pouvez maintenant vous connecter.');
                window.location.href = 'login.html';
            } else {
                alert(data.message || 'Erreur lors de l\'inscription');
            }
        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur lors de l\'inscription');
        }
    });
}

function updateNavButtons() {
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    const navButtons = document.querySelector('.nav-buttons');
    
    if (navButtons) {
        if (token) {
            navButtons.innerHTML = `
                <span style="color: white; margin-right: 10px;">Bienvenue, ${username}</span>
                <button onclick="logout()" class="nav-buttons button">Déconnexion</button>
            `;
        } else {
            navButtons.innerHTML = `
                <button onclick="window.location.href='login.html'" class="nav-buttons button">Connexion</button>
                <button onclick="window.location.href='register.html'" class="nav-buttons button">Inscription</button>
            `;
        }
    }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    window.location.href = 'login.html';
}

document.addEventListener('DOMContentLoaded', updateNavButtons);

// Fonction pour afficher les notifications
function showNotification(message, type = 'error') {
    // Supprimer toute notification existante
    const existingNotif = document.querySelector('.notification');
    if (existingNotif) {
        existingNotif.remove();
    }

    // Créer la nouvelle notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    // Ajouter au DOM
    document.body.appendChild(notification);

    // Afficher avec animation
    setTimeout(() => notification.classList.add('show'), 10);

    // Supprimer après 3 secondes
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Gestion du formulaire de connexion
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Validation basique
        if (!username || !password) {
            showNotification('Veuillez remplir tous les champs', 'error');
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('username', username);
                showNotification('Connexion réussie!', 'success');
                setTimeout(() => window.location.href = 'index.html', 1000);
            } else {
                showNotification(data.message || 'Erreur de connexion', 'error');
            }
        } catch (error) {
            console.error('Erreur:', error);
            showNotification('Erreur de connexion au serveur', 'error');
        }
    });
}

// Gestion du formulaire d'inscription
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        // Validations
        if (!username || !email || !password || !confirmPassword) {
            showNotification('Veuillez remplir tous les champs', 'error');
            return;
        }

        if (password.length < 6) {
            showNotification('Le mot de passe doit contenir au moins 6 caractères', 'error');
            return;
        }

        if (password !== confirmPassword) {
            showNotification('Les mots de passe ne correspondent pas', 'error');
            return;
        }

        if (!email.includes('@')) {
            showNotification('Veuillez entrer une adresse email valide', 'error');
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            });

            const data = await response.json();

            if (response.ok) {
                showNotification('Inscription réussie!', 'success');
                setTimeout(() => window.location.href = 'login.html', 1000);
            } else {
                showNotification(data.message || 'Erreur lors de l\'inscription', 'error');
            }
        } catch (error) {
            console.error('Erreur:', error);
            showNotification('Erreur de connexion au serveur', 'error');
        }
    });
}

function updateNavButtons() {
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    const navButtons = document.querySelector('.nav-buttons');
    
    if (navButtons) {
        if (token) {
            navButtons.innerHTML = `
                <span style="color: white; margin-right: 10px;">Bienvenue, ${username}</span>
                <button onclick="logout()" class="login-btn">Déconnexion</button>
            `;
        } else {
            navButtons.innerHTML = `
                <button onclick="window.location.href='login.html'" class="login-btn">Connexion</button>
                <button onclick="window.location.href='register.html'" class="signup-btn">Inscription</button>
            `;
        }
    }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    showNotification('Déconnexion réussie', 'success');
    setTimeout(() => {
        window.location.href = 'login.html';
    }, 1000);
}

document.addEventListener('DOMContentLoaded', updateNavButtons);