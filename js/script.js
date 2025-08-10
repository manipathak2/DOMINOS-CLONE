let cart = JSON.parse(localStorage.getItem("cart")) || [];

function addToCart(item, price) {
  cart.push({ item, price });
  localStorage.setItem("cart", JSON.stringify(cart));
  alert(item + " added to cart!");
}

function checkout() {
  alert("Order placed!");
  cart = [];
  localStorage.setItem("cart", JSON.stringify(cart));
}

window.onload = function () {
  const cartContainer = document.getElementById("cart-items");
  if (cartContainer) {
    cartContainer.innerHTML = cart.map(
      c => `<p>${c.item} - ₹${c.price}</p>`
    ).join("");
  }

// Update localStorage
function saveCart() {
  localStorage.setItem("cart", JSON.stringify(cart));
}
}
