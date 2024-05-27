from pymongo import MongoClient

# Detalles de conexión a MongoDB
MONGO_HOST = "10.128.0.97"
MONGO_PORT = 27017
MONGO_USER = "tarjetas_user"
MONGO_PASS = "isis2503"

# URL de conexión
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"

# Conexión a MongoDB
client = MongoClient(MONGO_URI)
db = client.mydatabase  # Nombre de la base de datos
collection = db.mycollection  # Nombre de la colección


for document in collection.find():
    print(document)

# Consultar un documento específico en la colección
# Por ejemplo, el primer documento que cumple con ciertas condiciones
result = collection.find_one({"name": "John"})
print(result)