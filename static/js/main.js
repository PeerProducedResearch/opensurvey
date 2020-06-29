// Toggle mobile menu
const burgerMenu = document.getElementById("burger-menu");
const navbar = document.getElementById("navbar");
const body = document.body;
let navbarStatus = false;

burgerMenu.addEventListener("click", function toggleMenu() {
  if (!navbarStatus) {
    const scrollY = document.documentElement.style.getPropertyValue(
      "--scroll-y"
    );
    navbar.classList.add("isOpen");
    navbarStatus = true;
    body.style.position = "fixed";
    body.style.top = `-${scrollY}`;
  } else {
    const scrollY = body.style.top;
    navbar.classList.remove("isOpen");
    navbarStatus = false;
    body.style.position = "";
    body.style.top = "";
    window.scrollTo(0, parseInt(scrollY || "0") * -1);
  }
});

let prevScrollpos = window.pageYOffset;
const header = document.getElementById("header");

window.onscroll = function () {
  // needed for scroll position after closing the popup
  document.documentElement.style.setProperty(
    "--scroll-y",
    `${window.scrollY}px`
  );
  // Menu hide and show
  let currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    // When the user scrolls up, show the navbar
    header.classList.add("isVisible");
    if (prevScrollpos > 500) {
      // Add a background to the navbar below 500px
      header.classList.add("hasBackground");
    } else {
      header.classList.remove("hasBackground");
    }
  } else if (!navbarStatus) {
    // // When the user scrolls down, hide the navbar. Don't hide navbar when mobile menu is open.
    header.classList.remove("isVisible");
  }
  prevScrollpos = currentScrollPos;
};
