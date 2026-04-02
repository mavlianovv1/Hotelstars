function sortFlights(type) {
  const list = document.getElementById('flights-list');
  const cards = Array.from(list.querySelectorAll('.flight-card'));

  cards.sort((a, b) => {
    const pA = parseFloat(a.dataset.price);
    const pB = parseFloat(b.dataset.price);
    const rA = parseFloat(a.dataset.rating);
    const rB = parseFloat(b.dataset.rating);

    if (type === 'cheap') return pA - pB;
    if (type === 'rating') return rB - rA;
    if (type === 'fast') return pA - pB;

    return 0;
  });

  cards.forEach(card => list.appendChild(card));
}

function sortFlights(type) {
  let container = document.getElementById("flights-list");
  let cards = Array.from(container.getElementsByClassName("flight-card"));

  cards.sort((a, b) => {
    if (type === "cheap") {
      return a.dataset.price - b.dataset.price;
    }

    if (type === "rating") {
      return b.dataset.rating - a.dataset.rating;
    }

    return 0;
  });

  container.innerHTML = "";
  cards.forEach(card => container.appendChild(card));
}
