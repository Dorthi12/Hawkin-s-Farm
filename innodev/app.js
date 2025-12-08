
const productsData = [
  {
    name: "Wheat - Sharbati",
    farmer: "Dorthi Raj",
    location: "Bareilly",
    qty: 500,
    price: 24,
    img: "https://via.placeholder.com/300x150?text=Wheat"
  },
  {
    name: "Basmati Rice",
    farmer: "Akanksha",
    location: "Lucknow",
    qty: 300,
    price: 59,
    img: "https://via.placeholder.com/300x150?text=Rice"
  }
];


const ordersData = [
  {
    id: "ORD101",
    crop: "Wheat - Sharbati",
    buyer: "Rahul Verma",
    qty: 200,
    total: 4800,
    status: "In Transit",
    date: "10 Feb 2025"
  },
  {
    id: "ORD092",
    crop: "Basmati Rice",
    buyer: "Neha Sharma",
    qty: 150,
    total: 8700,
    status: "Delivered",
    date: "06 Feb 2025"
  }
];


const currentPage = window.location.pathname.split("/").pop();


if (currentPage === "products.html") {
  const grid = document.querySelector(".product-grid");

  productsData.forEach((p) => {
    const card = document.createElement("a");
    card.href = "orders.html";
    card.style.textDecoration = "none";
    card.style.color = "inherit";

    card.innerHTML = `
      <div class="card product-card">
        <img src="${p.img}" />
        <h3>${p.name}</h3>
        <p>Farmer: ${p.farmer}</p>
        <p>Location: ${p.location} · ${p.qty}kg</p>
        <p class="price">₹ ${p.price} / kg</p>
        <button class="btn btn-primary full-width" style="margin-top: 6px;">
          View & Buy
        </button>
      </div>
    `;

   
    grid.appendChild(card);
  });
}


if (currentPage === "orders.html") {
  const tbody = document.querySelector("#orders-body");

  ordersData.forEach((o) => {
    const tr = document.createElement("tr");

    tr.innerHTML = `
      <td>${o.id}</td>
      <td>${o.crop}</td>
      <td>${o.buyer}</td>
      <td>${o.qty}</td>
      <td>₹ ${o.total}</td>
      <td>${o.status}</td>
      <td>${o.date}</td>
    `;

    tbody.appendChild(tr);
  });
}


function getCurrentUser() {
  const user = localStorage.getItem("user");
  return user ? JSON.parse(user) : null;
}

// LOGIN PAGE
const loginForm = document.querySelector("#login-form");
if (loginForm) {
  loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const email = loginForm.querySelector('input[type="email"]').value;

    // sirf demo ke liye: jo bhi email de, usko login maan lo
    const user = { email, role: "farmer" };
    localStorage.setItem("user", JSON.stringify(user));

    window.location.href = "dashboard.html";
  });
}

// REGISTER PAGE
const registerForm = document.querySelector("#register-form");
if (registerForm) {
  registerForm.addEventListener("submit", (e) => {
    e.preventDefault();
    alert("Registered! Please login.");
    window.location.href = "login.html";
  });
}

// PROTECTED PAGES (dashboard, products, upload, orders)
const protectedPages = [
  "dashboard.html",
  "products.html",
  "upload.html",
  "orders.html"
];

if (protectedPages.includes(currentPage) && !getCurrentUser()) {
  // not logged in → send to login
  window.location.href = "login.html";
}
