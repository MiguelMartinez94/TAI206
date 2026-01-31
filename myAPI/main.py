#Importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional
#Inicialización del servidor
app = FastAPI(
    title = 'Mi primer API',
    description = 'Esta es mi primera API',
    version = '1.0'
    
)

usuarios = [
    
    {
        "id":1,
        "nombre":"Miguel",
        "edad":"23"
    },
    
    {
        "id":2,
        "nombre":"Ximena",
        "edad":"18"
    },
    
    {
        "id":3,
        "nombre":"Joanna",
        "edad":"20"
    },
]

#Endpoints
@app.get('/', tags=['Inicio'])
async def holamundo():
    return {"mensaje":"Hola mundo con FastAPI"}

@app.get("/bienvenidos", tags=['Inicio'])
async def bienvenido():
    return {"mensaje":"Bienvenidos a tu API REST"}

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    
    await asyncio.sleep(5)
    return {"mensaje":"Las califiación en TAI es 10"}

@app.get("/v1/usuario/{id}", tags=['Parametro Obligatorio'])
async def consultaUsuarios(id:int):
    return {"Usuario encontrado":id}

@app.get("/v1/usuarios_op/", tags=['Parametro opcional'])
async def consultaOp(id:Optional[int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"usuario encontrado":id, "usuario":usuario}
        return {"mensaje":"usuario no encontrado"}
    else:
        return {"mensaje":"no se proporcionó id"}
    
    