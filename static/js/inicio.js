let map = L.map("map").setView([-33.447487,  -70.673676], 5);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

fetch("http://localhost:5000/get-don-map-data")
  .then((response) => response.json())
  .then((parsedData) => {
    var markers = L.markerClusterGroup();
    for (let don of parsedData) {
      let lat = don["lat"];
      let lng = don["long"];

      const onMarkerClick = (e) => {
        L.popup()
          .setLatLng([lat, lng])
          .setContent(
            `<h3>Donación n°${don["id"]}:</h3>
            <b>Calle y número:</b> ${don["calle"]}<br>
            <b>Tipo:</b> ${don["tipo"]}<br>
            <b>Cantidad:</b> ${don["cantidad"]}<br>
            <b>Fecha disponibilidad:</b> ${don["fecha"]}<br>
            <b>Email:</b> ${don["email"]}`
          )
          .openOn(map);
      };

      let marker = L.marker([lat, lng]).addTo(map);
      marker.on("click", onMarkerClick);
      markers.addLayer(marker);
    }
    map.addLayer(markers);
  });

var violetIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-violet.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

fetch("http://localhost:5000/get-ped-map-data")
  .then((response) => response.json())
  .then((parsedData) => {
    var markers = L.markerClusterGroup();
    for (let ped of parsedData) {
      let lat = ped["lat"];
      let lng = ped["long"];

      const onMarkerClick = (e) => {
        L.popup()
          .setLatLng([lat, lng])
          .setContent(
            `<h3>Pedido n°${ped["id"]}:</h3>
            <b>Tipo:</b> ${ped["tipo"]}<br>
            <b>Cantidad:</b> ${ped["cantidad"]}<br>
            <b>Email:</b> ${ped["email"]}`
          )
          .openOn(map);
      };

      let marker = L.marker([lat, lng], {icon: violetIcon}).addTo(map);
      marker.on("click", onMarkerClick);
      markers.addLayer(marker);
    }
    map.addLayer(markers);
  });













const aDon = () => {
    window.location.href = "../html/agregar-donacion.html"
}

const aPed = () => {
    window.location.href = "../html/agregar-pedido.html"
}

const vDon = () => {
    window.location.href = "../html/ver-donaciones.html"
}

const vPed = () => {
    window.location.href = "../html/ver-pedidos.html"
}


//let agregarDon = document.getElementById("agregarD");
//agregarDon.addEventListener("click",aDon );

let agregarPed = document.getElementById("agregarP");
agregarPed.addEventListener("click", aPed );

let verDon = document.getElementById("verD");
verDon.addEventListener("click",vDon );

let verPed = document.getElementById("verP");
verPed.addEventListener("click", vPed );

