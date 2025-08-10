// Cart JS - Updated

let cart = JSON.parse(localStorage.getItem("cart")) || [];

// Save cart to localStorage
function saveCart() {
  localStorage.setItem("cart", JSON.stringify(cart));
}

// Add item to cart
function addToCart(item, price) {
  const existing = cart.find(c => c.item === item);
  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({ item, price, qty: 1 });
  }
  saveCart();
  alert(item + " added to cart!");

  updateCartIcon();
}

// Increase quantity
function increaseQty(index) {
  cart[index].qty += 1;
  saveCart();
  renderCart();
}

// Decrease quantity
function decreaseQty(index) {
  if (cart[index].qty > 1) {
    cart[index].qty -= 1;
  } else {
    cart.splice(index, 1);
  }
  saveCart();
  renderCart();
  updateCartIcon();
}

// Checkout function
function checkout() {
  if (cart.length === 0) {
    alert("Cart is empty!");
    return;
  }
  alert("Order placed successfully!");
  cart = [];
  saveCart();
  renderCart();
  updateCartIcon();
}

// Update cart icon count
function updateCartIcon() {
  const cartIcon = document.querySelector(".cart-icon");
  if (cartIcon) {
    const totalItems = cart.reduce((sum, c) => sum + c.qty, 0);
    cartIcon.setAttribute("data-count", totalItems);
  }
}

// Render cart content
function renderCart() {
  const cartContainer = document.getElementById("cart-items");
  const totalContainer = document.getElementById("cart-total");

  if (!cartContainer || !totalContainer) return;

  if (cart.length === 0) {
    cartContainer.innerHTML = "<p>Your cart is empty.</p>";
    totalContainer.textContent = "Total: ₹0";
    return;
  }

  cartContainer.innerHTML = cart
    .map((c, index) => `
      <div class="cart-item">
        <div class="cart-item-info">
          <img src="image/${c.item.toLowerCase().replace(/\s+/g, "-")}.jpg" alt="${c.item}" onerror="this.style.display='none'">
          <div>
            <div class="cart-item-name">${c.item}</div>
            <div class="cart-item-price">₹${c.price}</div>
          </div>
        </div>
        <div class="quantity-control">
          <button onclick="decreaseQty(${index})">−</button>
          <span>${c.qty}</span>
          <button onclick="increaseQty(${index})">+</button>
        </div>
      </div>
    `)
    .join("");

  const total = cart.reduce((sum, c) => sum + c.price * c.qty, 0);
  totalContainer.textContent = `Total: ₹${total}`;
}

// Initialize on page load
window.onload = function () {
  renderCart();
  updateCartIcon();
};
