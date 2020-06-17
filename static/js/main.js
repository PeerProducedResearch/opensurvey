// Toggle mobile menu
const burgerMenu = document.getElementById("burger-menu");
const navbar = document.getElementById("navbar");

burgerMenu.addEventListener("click", function toggleMenu() {
  navbar.classList.toggle("isOpen");
});

/* When the user scrolls down, hide the navbar. When the user scrolls up, show the navbar */
let prevScrollpos = window.pageYOffset;
const header = document.getElementById("header");

window.onscroll = function () {
  let currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    header.classList.add("isVisible");
  } else {
    header.classList.remove("isVisible");
  }
  prevScrollpos = currentScrollPos;
};
