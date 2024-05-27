from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from models import User
import database

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit")
async def submit_form(name: str = Form(...), email: str = Form(...)):
    user = User(name=name, email=email)
    database.collection.insert_one(user.dict())
    return {"message": "Usuario guardado con éxito"}
