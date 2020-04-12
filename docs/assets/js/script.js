
// Get the navbar
var navbar = document.getElementById("topNav");

function addDrop() {
  if (navbar.classList.contains("drop")) {
    navbar.classList.remove("drop");
  } else {
    navbar.classList.add("drop");
  }
}

// When the user scrolls the page, execute myFunction
window.onscroll = function() {addSticky()};

// Get the offset position of the navbar
var sticky = navbar.offsetTop;

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function addSticky() {
  if (window.pageYOffset > sticky) {
    navbar.classList.add("sticky")
  } else {
    navbar.classList.remove("sticky");
  }
}