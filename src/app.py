# Importa las clases Flask, jsonify y request del módulo flask
from flask import Flask, jsonify, request
# Importa la clase CORS del módulo flask_cors
from flask_cors import CORS
# Importa la clase SQLAlchemy del módulo flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# Importa la clase Marshmallow del módulo flask_marshmallow
from flask_marshmallow import Marshmallow

# Crea una instancia de la clase Flask con el nombre de la aplicación
app = Flask(__name__)
# Configura CORS para permitir el acceso desde el frontend al backend
CORS(app)

# Configura la URI de la base de datos con el driver de MySQL, usuario, contraseña y nombre de la base de datos
# URI de la BD == Driver de la BD://user:password@UrlBD/nombreBD
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Admin1234.@localhost/proyecto"
# Configura el seguimiento de modificaciones de SQLAlchemy a False para mejorar el rendimiento
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

class Vehicle(db.Model):  # Vehicle hereda de db.Model
    """
    Definición de la tabla Vehicle en la base de datos.
    La clase Vehicle hereda de db.Model.
    Esta clase representa la tabla "Vehicle" en la base de datos y se definen sus campos.
    """
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    version = db.Column(db.String(100))
    color = db.Column(db.String(100))
    year = db.Column(db.Integer)
    serial = db.Column(db.String(100))
    patent = db.Column(db.String(100))
    price = db.Column(db.Double)
    dateAdmission = db.Column(db.DateTime)
    dateSale = db.Column(db.DateTime)
    image = db.Column(db.String(400))

    def __init__(self, brand, model, version, color, year, serial, patent, price, dateAdmission, dateSale, image):
        """
        Constructor de la clase Producto.

        Args:
            brand (str): Marca del vehículo.
            model (str): Modelo del vehículo.
            version (str): Versión del vehículo.
            color (str): Color del vehículo.
            year (int): Año del vehículo.
            serial (str): Serial del vehículo.
            patent (str): Patenta del vehículo.
            price (decimal): Precio del vehículo.
            dateAdmission (datetime): Fecha de ingreso del vehículo.
            dateSale (datetime): Fecha de venta del vehículo.
            image (str): URL o ruta de la imagen del producto.
        """
        self.brand = brand
        self.model = model
        self.version = version
        self.color = color
        self.year = year
        self.serial = serial
        self.patent = patent
        self.price = price
        self.dateAdmission = dateAdmission
        self.dateSale = dateSale
        self.image = image

with app.app_context():
    db.create_all()  # Crea todas las tablas en la base de datos

# Definición del esquema para la clase Vehicle
class VehicleSchema(ma.Schema):
    """
    Esquema de la clase Vehicle.

    Este esquema define los campos que serán serializados/deserializados
    para la clase Vehicle.
    """
    class Meta:
        fields = ("id", "brand", "model", "version", "color", "year", "serial", "patent", "price", "dateAdmission", "dateSale", "image")

vehicle_schema = VehicleSchema()  # Objeto para serializar/deserializar un vehiculos
vehicles_schema = VehicleSchema(many=True)  # Objeto para serializar/deserializar múltiples vehiculos

@app.route("/vehicles", methods=["GET"])
def get_Vehicles():
    """
    Endpoint para obtener todos los vehiculos de la base de datos.

    Retorna un JSON con todos los registros de la tabla de vehiculos.
    """
    all_vehicles = Vehicle.query.all()  # Obtiene todos los registros de la tabla de vehiculos
    result = vehicles_schema.dump(all_vehicles)  # Serializa los registros en formato JSON
    return jsonify(result)  # Retorna el JSON de todos los registros de la tabla

@app.route("/vehicles/<id>", methods=["GET"])
def get_vehicle(id):
    """
    Endpoint para obtener un vehiculo específico de la base de datos.

    Retorna un JSON con la información del vehiculo correspondiente al ID proporcionado.
    """
    vehicle = Vehicle.query.get(id)  # Obtiene el vehiculo correspondiente al ID recibido
    return vehicle_schema.jsonify(vehicle)  # Retorna el JSON del vehiculo

@app.route("/vehicles/<id>", methods=["DELETE"])
def delete_vehicle(id):
    """
    Endpoint para eliminar un vehiculo de la base de datos.

    Elimina el vehiculo correspondiente al ID proporcionado y retorna un JSON con el registro eliminado.
    """
    vehicle = Vehicle.query.get(id)  # Obtiene el vehiculo correspondiente al ID recibido
    db.session.delete(vehicle)  # Elimina el vehiculo de la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return vehicle_schema.jsonify(vehicle)  # Retorna el JSON del vehiculo eliminado

@app.route("/vehicles", methods=["POST"])  # Endpoint para crear un vehiculo
def create_vehicle():
    """
    Endpoint para crear un nuevo vehiculo en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro de vehiculo en la base de datos.
    Retorna un JSON con el nuevo vehiculo creado.
    """
    brand = request.json["brand"]  # Obtiene la marca del JSON proporcionado
    model = request.json["model"]  # Obtiene el modelo del JSON proporcionado
    version = request.json["version"]  # Obtiene la version del JSON proporcionado
    color = request.json["color"]  # Obtiene el color del JSON proporcionado
    year = request.json["year"]  # Obtiene el año del JSON proporcionado
    serial = request.json["serial"]  # Obtiene el serial del JSON proporcionado
    patent = request.json["patent"]  # Obtiene la patente del JSON proporcionado
    price = request.json["price"]  # Obtiene el precio del JSON proporcionado
    dateAdmission = request.json["dateAdmission"]  # Obtiene la fecha de ingreso del JSON proporcionado
    dateSale = request.json["dateSale"]  # Obtiene la fecha de venta del JSON proporcionado
    image = request.json["image"]  # Obtiene la imagen del JSON proporcionado
    new_vehicle = Vehicle(brand, model, version, color, year, serial, patent, price, dateAdmission, dateSale, image)  # Crea un nuevo objeto Vehicle con los datos proporcionados
    db.session.add(new_vehicle)  # Agrega el nuevo vehiculo a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return vehicle_schema.jsonify(new_vehicle)  # Retorna el JSON del nuevo vehiculo creado

@app.route("/vehicles/<id>", methods=["PUT"])  # Endpoint para actualizar un vehiculo
def update_vehicle(id):
    """
    Endpoint para actualizar un vehiculo existente en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro del vehiculo con el ID especificado.
    Retorna un JSON con el vehiculo actualizado.
    """
    vehicle = Vehicle.query.get(id)  # Obtiene el vehiculo existente con el ID especificado

    # Actualiza los atributos del producto con los datos proporcionados en el JSON
    vehicle.brand = request.json["brand"]
    vehicle.model = request.json["model"]
    vehicle.version = request.json["version"]
    vehicle.color = request.json["color"]
    vehicle.year = request.json["year"]
    vehicle.serial = request.json["serial"]
    vehicle.patent = request.json["patent"]
    vehicle.price = request.json["price"]
    vehicle.dateAdmission = request.json["dateAdmission"]
    vehicle.dateSale = request.json["dateSale"]
    vehicle.image = request.json["image"]

    db.session.commit()  # Guarda los cambios en la base de datos
    return vehicle_schema.jsonify(vehicle)  # Retorna el JSON del vehiculo actualizado

'''
Este código es el programa principal de la aplicación Flask. Se verifica si el archivo actual está siendo ejecutado directamente y no importado como módulo. Luego, se inicia el servidor Flask en el puerto 5000 con el modo de depuración habilitado. Esto permite ejecutar la aplicación y realizar pruebas mientras se muestra información adicional de depuración en caso de errores.

'''
# Programa Principal
if __name__ == "__main__":
    # Ejecuta el servidor Flask en el puerto 5000 en modo de depuración
    app.run(debug=True, port=5000)