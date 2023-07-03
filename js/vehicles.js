const { createApp } = Vue
createApp({
data() {
return {
vehicles:[],
//url:'http://localhost:5000/vehicles',
// si el backend esta corriendo local usar localhost 5000(si no lo subieron a pythonanywhere)
url:'https://alramos.pythonanywhere.com/vehicles', // si ya lo subieron a pythonanywhere
error:false,
cargando:true,
/*atributos para el guardar los valores del formulario */
id:0,
brand:"",
model:"",
version:"",
color:"",
year:"",
serial:"",
patent:"",
price:0,
dateAdmission:"",
dateSale:"",
image:"",
}
},
methods: {
fetchData(url) {
fetch(url)
.then(response => response.json())
.then(data => {
this.vehicles = data;
this.cargando=false
})
.catch(err => {
console.error(err);
this.error=true
})
},
deleteVehicle(vehicle) {
const url = this.url+'/' + vehicle;
var options = {
method: 'DELETE',
}
fetch(url, options)
.then(res => res.text()) // or res.json()
.then(res => {
location.reload();
})
},
create(){
let vehicle = {
brand:this.brand,
model: this.model,
version: this.version,
color: this.color,
year: this.year,
serial: this.serial,
patent: this.patent,
price: parseFloat(this.price),
dateAdmission: this.dateAdmission,
dateSale: this.dateSale,
image:this.image
}
var options = {
body:JSON.stringify(vehicle),
method: 'POST',
headers: { 'Content-Type': 'application/json' },
redirect: 'follow'
}
fetch(this.url, options)
.then(function () {
alert("Registro grabado")
window.location.href = "vehicles_list.html";
})
.catch(err => {
console.error(err);
alert("Error al Grabar")
})
}
},
created() {
this.fetchData(this.url)
},
}).mount('#app')