from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Detalles de conexión a MongoDB
MONGO_HOST = "10.128.0.97"
MONGO_PORT = 27017
MONGO_USER = "tarjetas_user"
MONGO_PASS = "isis2503"
MONGO_DB = "mydatabase"
MONGO_COLLECTION = "mycollection"

# URL de conexión
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"

# Conexión a MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

@app.get("/tarjetas/todaslastarjetas", response_class=HTMLResponse)
async def mostrar_todas_las_tarjetas(request: Request):
    # Obtener todas las tarjetas de la base de datos
    tarjetas = list(collection.find({}))

    # Renderizar la plantilla HTML con los datos obtenidos
    return templates.TemplateResponse("todas_lastarjetas.html", {"request": request, "tarjetas": tarjetas})
