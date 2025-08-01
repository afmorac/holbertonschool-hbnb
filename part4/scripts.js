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

  // Página index.html
  if (document.getElementById('places-list')) {
    checkAuthenticationIndex();
  }

  // Página place.html
  if (document.getElementById('place-details')) {
    checkAuthenticationPlace();
  }

  // Página add_review.html
  if (document.getElementById('review-form')) {
    checkAuthenticationAddReview();
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

// INDEX – Mostrar u ocultar botón Login + lugares
function checkAuthenticationIndex() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    loginLink.style.display = 'block';
  } else {
    loginLink.style.display = 'none';
    fetchPlaces(token);
  }
}

async function fetchPlaces(token) {
  const places = [
    { name: 'Apartamento en San Juan', price: 50 },
    { name: 'Casa en Bayamón', price: 100 },
    { name: 'Estudio en Ponce', price: 30 }
  ];

  displayPlaces(places);
  setupFilter(places);
}

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

// PLACE – Mostrar detalles si hay token
function checkAuthenticationPlace() {
  const token = getCookie('token');
  const addReviewSection = document.getElementById('add-review');
  const placeId = getPlaceIdFromURL();

  if (!token) {
    addReviewSection.style.display = 'none';
  } else {
    addReviewSection.style.display = 'block';
    fetchPlaceDetails(token, placeId);
  }
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id'); // Ejemplo: place.html?id=1
}

async function fetchPlaceDetails(token, placeId) {
  const place = {
    name: 'Apartamento en San Juan',
    host: 'Carlos Rodríguez',
    price: 75,
    description: 'Hermoso apartamento cerca del mar.',
    amenities: ['WiFi', 'Piscina', 'Aire Acondicionado'],
    reviews: [
      { user: 'Ana', comment: 'Muy cómodo', rating: 5 },
      { user: 'Luis', comment: 'Excelente ubicación', rating: 4 }
    ]
  };

  displayPlaceDetails(place);
}

function displayPlaceDetails(place) {
  const placeDetails = document.getElementById('place-details');
  placeDetails.innerHTML = `
    <div class="place-info">
      <h2>${place.name}</h2>
      <p><strong>Anfitrión:</strong> ${place.host}</p>
      <p><strong>Precio:</strong> $${place.price} por noche</p>
      <p><strong>Descripción:</strong> ${place.description}</p>
      <p><strong>Amenidades:</strong> ${place.amenities.join(', ')}</p>
    </div>
    <h3>Reseñas:</h3>
  `;

  place.reviews.forEach(review => {
    const reviewCard = document.createElement('div');
    reviewCard.className = 'review-card';
    reviewCard.innerHTML = `
      <p><strong>${review.user}</strong> - ⭐ ${review.rating}</p>
      <p>${review.comment}</p>
    `;
    placeDetails.appendChild(reviewCard);
  });
}

// ADD REVIEW – Validar, enviar review y redirigir si no está logueado
function checkAuthenticationAddReview() {
  const token = getCookie('token');
  if (!token) {
    window.location.href = 'index.html';
    return;
  }

  const placeId = getPlaceIdFromURL();
  const reviewForm = document.getElementById('review-form');

  reviewForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const reviewText = reviewForm.elements.review.value;
    const rating = reviewForm.elements.rating.value;

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          text: reviewText,
          rating: parseInt(rating)
        })
      });

      if (response.ok) {
        alert('Review enviada exitosamente');
        reviewForm.reset();
      } else {
        alert('Error al enviar la review');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('No se pudo conectar con el servidor');
    }
  });
}
