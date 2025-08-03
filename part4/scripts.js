document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const username = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();

      // Simulación de usuario local
      if (username === 'usuario1' && password === '123456') {
        document.cookie = `token=simulatedToken123; path=/`;
        window.location.href = 'index.html';
      } else {
        alert('Login failed: Credenciales inválidas');
      }
    });
  }

  if (document.getElementById('places-list')) {
    const token = getCookie('token');
    if (token) fetchPlaces();
  }
});

// Función para obtener cookies
function getCookie(name) {
  const cookieArr = document.cookie.split(';');
  for (let cookie of cookieArr) {
    const [key, value] = cookie.trim().split('=');
    if (key === name) return value;
  }
  return null;
}

async function fetchPlaces() {
  const response = await fetch('https://jsonplaceholder.typicode.com/posts');
  const data = await response.json();

  const places = data.slice(0, 3).map((item, index) => ({
    name: item.title,
    price: 100 + index * 50
  }));

  displayPlaces(places);
  setupFilter(places);
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';

  places.forEach((place, idx) => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.dataset.price = place.price;
    card.innerHTML = `
      <h3>${place.name}</h3>
      <p>Price per night: $${place.price}</p>
      <button class="details-button">View Details</button>
    `;
    placesList.appendChild(card);
  });
}

function setupFilter(places) {
  const filter = document.getElementById('price-filter');
  if (!filter) return;

  filter.addEventListener('change', () => {
    const maxPrice = filter.value;
    const cards = document.querySelectorAll('.place-card');

    cards.forEach(card => {
      const price = parseInt(card.dataset.price, 10);
      card.style.display = (maxPrice === 'all' || price <= parseInt(maxPrice)) ? 'block' : 'none';
    });
  });
}
