console.log(location.search) // lee los argumentos pasados a este formulario
var id=location.search.substr(4)
console.log(id)
const { createApp } = Vue
createApp({
data() {
return {
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
    // url:'http://promero.pythonanywhere.com/productos/'+id,
    url:'https://alramos.pythonanywhere.com/vehicles/'+id,
}
},
methods: {
fetchData(url) {
fetch(url)
.then(response => response.json())
.then(data => {

console.log(data)
this.brand = data.brand
this.model = data.model
this.version = data.version
this.color = data.color
this.year = data.year
this.serial = data.serial
this.patent = data.patent
this.price = parseFloat(data.price)
this.dateAdmission = data.dateAdmission
this.dateSale = data.dateSale
this.image = data.image
})
.catch(err => {
console.error(err);
this.error=true
})
},
edit() {
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
body: JSON.stringify(vehicle),
method: 'PUT',
headers: { 'Content-Type': 'application/json' },
redirect: 'follow'
}
fetch(this.url, options)
.then(function () {
alert("Registro modificado")
window.location.href = "vehicles_list.html";
})
.catch(err => {
console.error(err);
alert("Error al Modificar")
})
}
},
created() {
this.fetchData(this.url)
},
}).mount('#app')