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

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit")
async def submit_form(
    ingresos: float = Form(...),
    egresos: float = Form(...),
    pasivos: float = Form(...),
    variables_mercado: str = Form(...)
):
    # Aquí podrías implementar la lógica para determinar el perfil de tarjeta
    # basándote en los datos proporcionados.
    perfil, franquicia, cupo = determinar_tarjeta(ingresos, egresos, pasivos, variables_mercado)
    
    return {"message": f"Tarjeta aprobada: Perfil: {perfil}, Franquicia: {franquicia}, Cupo: {cupo}"}

def determinar_tarjeta(ingresos: float, egresos: float, pasivos: float, variables_mercado: str):
    # Aquí iría tu lógica para determinar el perfil de tarjeta y otros detalles
    # Por ahora, solo devolveremos valores de ejemplo
    perfil = "Standard"
    franquicia = "Visa"
    cupo = 5000
    return perfil, franquicia, cupo
