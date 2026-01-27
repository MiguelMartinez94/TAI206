#Importaciones
from fastapi import FastAPI

#Inicialización del servidor
app = FastAPI()


#Endpoints
@app.get('/')
async def holamundo():
    return {"mensaje":"Hola mundo con FastAPI"}

@app.get("/bienvenidos")
async def bienvenido():
    return {"mensaje":"Bienvenidos a tu API REST"}