
const donaciones = () => {
    window.location.href = "../html/ver-donaciones.html"
}

let dona = document.getElementById("don");
dona.addEventListener("click", donaciones );



var modal = document.getElementById("myModal");
var span = document.getElementsByClassName("close")[0];
let fotoD = document.getElementById("fotoD");

fotoD.onclick = function() {
  modal.style.display = "block";
}

span.onclick = function() {
modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}