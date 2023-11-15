
// const ini = () => {
//     window.location.href = "../html/inicio.html"
// }

// let inic = document.getElementById("inicio");
// inic.addEventListener("click", ini );



const detalle = () => {
    window.location.href = "../html/informacion-pedido.html"
}

let row = document.getElementsByTagName("td");
for (x in row) {
    row[x].addEventListener("click", detalle );
}