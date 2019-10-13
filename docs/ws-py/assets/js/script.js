
function addResponsive() {
  var x = document.getElementById("topNav");
  if (x.className === "navbar") {
    x.className += " responsive";
  } else {
    x.className = "navbar";
  }
}
