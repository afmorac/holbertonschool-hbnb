document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });

        if (response.ok) {
          const data = await response.json();
          document.cookie = `token=${data.access_token}; path=/`;
          window.location.href = 'index.html';
        } else {
          alert('Login failed');
        }
      } catch (error) {
        console.error('Error:', error);
        alert('Error al conectar con el servidor');
      }
    });
  }

  // Ejecutar solo si estamos en index.html
  if (document.getElementById('places-list')) {
    checkAuthentication();
  }
});

// Función para obtener el valor de una cookie
function getCookie(name) {
  const cookieArr = document.cookie.split(';');
  for (let cookie of cookieArr) {
    const [key, value] = cookie.trim().split('=');
    if (key === name) return value;
  }
  return null;
}

// Verifica si el usuario está autenticado y decide si mostrar el botón login
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    loginLink.style.display = 'block';
  } else {
    loginLink.style.display = 'none';
    fetchPlaces(token);
  }
}

// Simula datos de lugares (puedes cambiar esto por un fetch real si conectas el backend)
async function fetchPlaces(token) {
  const places = [
    { name: 'Apartamento en San Juan', price: 50 },
    { name: 'Casa en Bayamón', price: 100 },
    { name: 'Estudio en Ponce', price: 30 }
  ];

  displayPlaces(places);
  setupFilter(places);
}

// Muestra los lugares en la página como tarjetas
function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';

  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.dataset.price = place.price;
    card.innerHTML = `
      <h3>${place.name}</h3>
      <p>Precio por noche: $${place.price}</p>
      <button class="details-button">Ver detalles</button>
    `;
    placesList.appendChild(card);
  });
}

// Filtro de precios
function setupFilter(places) {
  const filter = document.getElementById('price-filter');
  filter.innerHTML = `
    <option value="all">Todos</option>
    <option value="10">Hasta $10</option>
    <option value="50">Hasta $50</option>
    <option value="100">Hasta $100</option>
  `;

  filter.addEventListener('change', () => {
    const maxPrice = filter.value;
    const cards = document.querySelectorAll('.place-card');

    cards.forEach(card => {
      const price = parseInt(card.dataset.price, 10);
      if (maxPrice === 'all' || price <= parseInt(maxPrice)) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  });
}
