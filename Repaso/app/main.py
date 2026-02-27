from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import Literal
from datetime import datetime

app= FastAPI(
    title="Biblioteca Repaso",
    description="En este ejercicio es un repaso de clases pasadas"
)

class libro(BaseModel):
    id_libro:int
    nombre_libro:str = Field(min_length=2, max_length=100)
    autor:str
    anio: int = Field(gt=1450, le=datetime.now().year)
    paginas:int = Field(gt=1)
    estado:Literal["disponible", "prestado"]
    
class prestamo(BaseModel):
    id_prestamo:int
    id_libro:int
    id_estudiante:int
    
    
class estudiante(BaseModel):
    id_estudiante:int
    nombre_estudiante:str = Field(min_length=2)  
    correo: EmailStr

libros =[]

prestamos = []

estudiantes = [
    {
        "id_estudiante":1,
        "nombre_estudiante":"Miguel",
        "correo":"guelo0203@gmail.com"
    }
] 

@app.get("/")
async def home():
    return {"mensaje":"Ya jaló"}

@app.get("/v1/libro/buscar/{nombre_libro}", tags=['Libros'])
async def nombreLibro(nombre_libro:str):
    for lib in libros:
        if lib["nombre_libro"].lower().strip() == nombre_libro.lower().strip():
            return {
                "mensaje":"Libro encontrado",
                "libro":lib
            }
    raise HTTPException(status_code=404, detail="Libro no encontrado")
    

@app.get("/v1/libros", tags=['Libros'])
async def getLibros():
        
        if libros:
                
                return {
                    "status":200,
                    "mensaje":"Libros encontrados",
                    "total": len(libros),
                    "libro":libros
                }
        
        raise HTTPException(status_code=404, detail="Libros no encontrados o inexistentes")
    
@app.post("/v1/libros", tags=['Libros'])
async def postLibro(nuevo_libro:libro):
    for lib in libros:
        if lib["id_libro"] == nuevo_libro.id_libro:
            
            raise HTTPException(status_code=400, detail="Este libro ya existe")
    
    libro_dict= nuevo_libro.model_dump()        
    libros.append(libro_dict) 
    return {
        "status":201,
        "libro":libro_dict,
        "mensaje":"Libro agregado"
    }
    
    
@app.post("/v1/prestamos/", tags=['Prestamos'])
async def registrarPrestamo(nuevo_prestamo:prestamo):
    
    for p in prestamos:
        if p["id_prestamo"] == nuevo_prestamo.id_prestamo:
            raise HTTPException(status_code=400, detail="El prestamo ya existe")
    
    
    estudiante_registrado = False
    for e in estudiantes:
        if e["id_estudiante"] == nuevo_prestamo.id_estudiante:
            estudiante_registrado = True
            
    if not estudiante_registrado:
        raise HTTPException(status_code=404, detail="Estudiante no está registrado")
    
    libro_prestado=None
    for lib in libros:
        if lib["id_libro"] == nuevo_prestamo.id_libro:
            libro_prestado = lib
        
        if libro_prestado["estado"] == "prestado":
            raise HTTPException(status_code=409, detail="El libro ya está prestado")
    
    if not libro_prestado:        
        raise HTTPException(status_code=404, detail="El libro no existe")

    libro_prestado ["estado"] = "prestado"
    prestamos.append(nuevo_prestamo.model_dump())
    
    return {
        "status":201,
        "mensaje":"Préstamo registrado con éxito",
        "prestamo":nuevo_prestamo,
        "Libro":libro_prestado
    }
@app.put("/v1/prestamos/devolver/{id_prestamo}", tags=['Prestamos'])
async def devolverLibro(id_prestamo:int):
    
    for p in prestamos:
        if p["id_prestamo"] == id_prestamo:
            
            for lib in libros:
                if lib ["id_libro"] == p["id_libro"]:
                    lib["estado"] = "disponible"
                    
                    return {
                        "status" : 200,
                        "mensaje": f"El libro {lib['nombre_libro']} ha sido devuelto"
                    }
            
    raise HTTPException(status_code=404, detail="No se encontró el préstamo")


@app.delete("/v1/prestamos/{id_prestamo}", tags=['Prestamos'])
async def eliminarPrestamo(id_prestamo:int):
    
    for p in prestamos:
        
        if p["id_prestamo"] == id_prestamo:
            prestamos.remove(p)
            
            return {
            "status": 200,
            "mensaje": "Registro de préstamo eliminado"
            }
    raise HTTPException(status_code=409, detail="No se encontró el registro")
            
                    