from pymongo import MongoClient

#Conexion con el servidor de mongodb 
MONGO_URI = 'mongodb://localhost'
client = MongoClient(MONGO_URI)

#Creacion de db
db = client['test_prueba']

#Creando las colecciones
collection_socios = db['socios']
collection_planes = db['planes']
collection_descuentos = db['descuentos']
collection_pagos = db['pagos']

#collection_socios.delete_many({})
#collection_descuentos.delete_many({})
#collection_pagos.delete_many({})
#collection_planes.delete_many({})