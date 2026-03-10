#Importaciones
from fastapi import FastAPI, HTTPException, status, Depends
import asyncio  
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from datetime import datetime



app = FastAPI()

security = HTTPBasic()

def verificacion(credentials:HTTPBasicCredentials=Depends()):
    
    usuario_auth = secrets.compare_digest(credentials.username, "root")
    pass_auth = secrets.compare_digest(credentials.password, "1234")
    
    if not (usuario_auth and pass_auth):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No tienes autorización")
    
    return credentials.username


citas = []

class cita(BaseModel):
    id:int #= Field (..., gt=0, examples=1)
    fecha : str
    nombre_paciente: str #= Field (..., min_length=5, examples="Miguel")
    motivo:str #= Field (..., le=100, examples="Gripe")
    confirmacion:bool = False
    
    

@app.get("/citas")
async def listarCitas():
    
    if not citas:
        raise HTTPException(status_code=404, detail="No hay citas")
    
    return {
        "Status":200,
        "citas": citas
    }
    
@app.get("/citas/{id}")
async def consultarID(id:int):
    
    for cita in citas:
        if cita["id"] == id:
        
            return {
                "cita_consultada":cita
            }
            
    raise HTTPException(status_code=404, detail="La cita que intenta consultar no existe")
    
    
@app.post("/citas")
async def crearCitas(cita:cita):
    for cita in citas:
        
        if cita["id"] == cita.id:
            
            raise HTTPException(status_code=400, detail="El usuario ya existe")
        
    
    citas.append(cita)    
    return{
        "status":201,
        "mensaje":"Cita agregada correctamente",
        "cita": cita
    }

@app.delete("/citas/{id}")
async def eliminarCitas(id:int):
    
    for cita in citas:
        if cita["id"] == id:
            citas.remove(cita)
            
            return{
                "mensaje":"Cita eliminada",
                "status":200
            }
    
    raise HTTPException(
        status_code=404,
        detail="La cita no existe"
    )
    
@app.put("/citas/{id}")
async def confirmarCita(id:int, cita:cita):
    
    for cita in citas:
        
        if cita.id == id:
            
            cita.id = True
            
    raise HTTPException(status_code=404, detail="Cita no encontrada")
