from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

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
    tipo_tarjeta: str = Form(...)
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
    
    return templates.TemplateResponse("result.html", {"request": request, "perfil": perfil, "franquicia": franquicia, "cupo": cupo})

def calcular_cupo(perfil: str) -> int:
    if perfil == "Negra":
        return 10000
    elif perfil == "Oro":
        return 5000
    else:
        return 2000
