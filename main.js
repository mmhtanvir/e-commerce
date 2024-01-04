var swiper = new Swiper('.swiper-container', {
  slidesPerView: 4,
  spaceBetween: 10,
  // Responsive breakpoints
  breakpoints: {
    // when window width is >= 320px
    320: {
      slidesPerView: 2,
      spaceBetween: 20
    },
    // when window width is >= 480px
    480: {
      slidesPerView: 2,
      spaceBetween: 20
    },
    // when window width is >= 640px
    768: {
      slidesPerView: 3,
      spaceBetween: 40
    },
    769: {
      slidesPerView: 4,
      spaceBetween: 40
    }
  },
  navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
  },
  pagination: {
      el: '.swiper-pagination',
      clickable: false,
  },
});

var buttons = document.querySelectorAll('.showPopupButton');

// Loop through each button and add event listeners
buttons.forEach(function(button) {
  button.addEventListener('click', function() {
      // Get the popup ID from the data-popup-id attribute
      var popupId = button.getAttribute('data-popup-id');

      // Call the showPopup function with the specific popup ID
      showPopup(popupId);
  });
});

function showPopup(popupId) {
var popup = document.getElementById(popupId);
var body = document.body;

// Add styles to stop scrolling
body.style.overflow = 'hidden';
body.style.paddingRight = '17px'; // Width of scrollbar

popup.classList.remove('hidden');
}

function hidePopup() {
var popups = document.getElementsByClassName("common");
var body = document.body;

// Remove styles to allow scrolling
body.style.overflow = 'visible';
body.style.paddingRight = '0';

// Loop through each popup and add the 'hidden' class
for (var i = 0; i < popups.length; i++) {
  popups[i].classList.add('hidden');
}
}



// JavaScript for changing quantity
function changeQuantity(amount) {
var quantityElement = document.getElementById("quantity");
var totalPriceElement = document.getElementById("totalPrice");

// Get the current quantity value
var currentQuantity = parseInt(quantityElement.innerText);

// Update the quantity based on the amount (1 for increment, -1 for decrement)
var newQuantity = currentQuantity + amount;

// Ensure the new quantity is within bounds (you can adjust this based on your requirements)
if (newQuantity < 1) {
    newQuantity = 1;
} else if (newQuantity > 24) {
    newQuantity = 24;
}

// Update the quantity element with the new value
quantityElement.innerText = newQuantity;

// Get the unit price from the DOM (assuming it's in the same structure)
var unitPriceElement = document.querySelector(".flex.items-center.space-x-4 h3.text-3xl");
var unitPrice = parseInt(unitPriceElement.innerText);

// Calculate the new total price based on the unit price and quantity
var newTotalPrice = unitPrice * newQuantity;

// Update the total price element with the new value
totalPriceElement.innerText = newTotalPrice + "tk";
}



// const swiper = new Swiper('.swiper-container', {
//     // Default parameters
//     slidesPerView: 1,
//     spaceBetween: 10,
//     // Responsive breakpoints
//     breakpoints: {
//       // when window width is >= 320px
//       320: {
//         slidesPerView: 2,
//         spaceBetween: 20
//       },
//       // when window width is >= 480px
//       480: {
//         slidesPerView: 3,
//         spaceBetween: 30
//       },
//       // when window width is >= 640px
//       640: {
//         slidesPerView: 4,
//         spaceBetween: 40
//       }
//     }
//   })