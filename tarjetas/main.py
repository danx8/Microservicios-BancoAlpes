from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import get_database_collection

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Obtener la colección de la base de datos
collection = get_database_collection()

class User(BaseModel):
    ingresos: float
    egresos: float
    pasivos: float
    variables_mercado: str

@app.get("/tarjetas", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/tarjetas/submit")
async def submit_form(
    request: Request,
    ingresos: float = Form(...),
    egresos: float = Form(...),
    pasivos: float = Form(...),
    variables_mercado: str = Form(...),
    tipo_tarjeta: str = Form(...),
    gmail: str = Form(...)
):
    saldo = ingresos - egresos
    if saldo < 0:
        perfil = "Negra"
    elif saldo > 1000:
        perfil = "Oro"
    else:
        perfil = "Plata"
    
    if tipo_tarjeta.lower() == "visa":
        franquicia = "Visa"
    else:
        franquicia = "MasterCard"
        
    cupo = calcular_cupo(perfil)
    
    return templates.TemplateResponse("result.html", {"request": request, "perfil": perfil, "franquicia": franquicia, "cupo": cupo, "gmail": gmail})

def calcular_cupo(perfil: str) -> int:
    if perfil == "Negra":
        return 10000
    elif perfil == "Oro":
        return 5000
    else:
        return 2000
    
@app.get("/tarjetas/todaslastarjetas", response_class=HTMLResponse)
async def mostrar_todas_las_tarjetas(request: Request):
    # Obtener todas las tarjetas de la base de datos
    tarjetas = list(collection.find({}))

    # Renderizar la plantilla HTML con los datos obtenidos
    return templates.TemplateResponse("todas_lastarjetas.html", {"request": request, "tarjetas": tarjetas})
