from fastapi import APIRouter
from typing import Optional
from app.data.database import usuarios
import asyncio

router = APIRouter(
    tags=["Miscelanious"]
)

@router.get("/usuarios_op/", tags=['Parametro opcional'])
async def consultaOp(id:Optional[int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"usuario encontrado":id, "usuario":usuario}
        return {"mensaje":"usuario no encontrado"}
    else:
        return {"mensaje":"no se proporcionó id"}

@router.get("/bienvenidos", tags=['Inicio'])
async def bienvenido():
    return {"mensaje":"Bienvenidos a tu API REST"}

@router.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    
    await asyncio.sleep(5)
    return {"mensaje":"Las califiación en TAI es 10"}

@router.get("/v1/usuario/{id}", tags=['Parametro Obligatorio'])
async def consultaUsuarios(id:int):
    return {"Usuario encontrado":id}
