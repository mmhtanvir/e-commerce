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

document.getElementById('cart-icon').addEventListener('click', function () {
document.getElementById('cart-box').classList.toggle('hidden');
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