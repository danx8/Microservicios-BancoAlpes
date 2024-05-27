from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import database  # Importa la configuración de la base de datos

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    name: str
    email: str

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit")
async def submit_form(name: str = Form(...), email: str = Form(...)):
    user = User(name=name, email=email)
    database.collection.insert_one(user.dict())
    return {"message": "Usuario guardado con éxito"}
