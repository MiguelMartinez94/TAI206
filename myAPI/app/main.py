#Importaciones
from fastapi import FastAPI, HTTPException, status
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
#@app.get('/', tags=['Inicio'])
#async def holamundo():
#    return {"mensaje":"Hola mundo con FastAPI"}

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
    
    
    
@app.get("/v1/usuarios/", tags=['CRUD Usuarios'])
async def consultarUsuarios():
    return usuarios
    
@app.post("/v1/usuarios/", tags=['CRUD Usuarios'])
async def agregar_usuarios(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            
            raise HTTPException(
                status_code=400, #Un error del cliente
                detail= "El usuario ya existe"
            )
        
    usuarios.append(usuario)
    return {
        "mensaje":"Usuario agregado",
        "datos":usuario,
        "status":"200"
    }
    
@app.put("/v1/usuarios/{id}", tags = ['CRUD Usuarios'])
async def actualizar_usuarios(id:int, usuario:dict):
    for user in usuarios:
        if user["id"] == id:
            
            user.update({
                "nombre" : usuario.get("nombre"),
                "edad" : usuario.get("edad")
            })
            
            return{
                "mensaje":"Usuario actualizado",
                "datos":user,
                "status": 200
                
            }
        
    raise HTTPException(
        status_code=404,
        detail="EL usuario no existe"
        )
    
    
@app.delete("/v1/usuarios/{id}", tags = ['CRUD Usuarios'])
async def eliminar_usuario(id:int):
    
    for user in usuarios:
        if user["id"] == id:
            usuarios.remove(user)
            
            return{
                "mensaje":"Usuario eliminado",
                "status":200
            }
    
    raise HTTPException(
        status_code=404,
        detail="El usuario no existe"
    )
        
    