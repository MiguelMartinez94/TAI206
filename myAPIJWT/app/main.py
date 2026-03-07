#Importaciones
from fastapi import FastAPI, HTTPException, status, Depends
import asyncio  
from typing import Optional
from pydantic import BaseModel, Field
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone

#Inicialización del servidor
app = FastAPI(
    title = 'Mi primer API',
    description = 'Esta es mi primera API',
    version = '1.0'
    
)

SECRET_KEY = "12345678"
ALGORITHM = "HS256"
hash_password = PasswordHash.recommended()

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

accesos = {
    "miguel": {
        "usuario": "miguel",
        "contraseña_hash": hash_password.hash("12345678")
    }}


oauth2_esquema = OAuth2PasswordBearer(tokenUrl="autorizacion")

#Modelo de validacion Pydantic

class UsuarioBase(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario", example="1")
    nombre: str = Field(...,min_length=3, max_length=50, description="Nombre del usuario")
    edad: int = Field(..., ge=0, le=121, description="Edad validad 0 y 121")

async def obtener_usuario_actual(token:str = Depends(oauth2_esquema)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario: str = payload.get("sub")
        if usuario is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )
        return usuario
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )


#Endpoints
#@app.get('/', tags=['Inicio'])
#async def holamundo():
#    return {"mensaje":"Hola mundo con FastAPI"}

@app.post("/autorizacion", tags=["Autenticacion"])
async def autorizacion(form_data: OAuth2PasswordRequestForm = Depends()):
    acceso = accesos.get(form_data.username)
    
    if not acceso or not hash_password.verify(form_data.password, acceso["contraseña_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    hora_expiracion = datetime.now(timezone.utc) + timedelta(minutes=1)
    payload = {
        "sub":acceso["usuario"],
        "exp":hora_expiracion
    }
    
    token= jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token":token,
        "token_type":"bearer"
    }

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
async def agregar_usuarios(usuario:UsuarioBase):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            
            raise HTTPException(
                status_code=400, #Un error del cliente
                detail= "El usuario ya existe"
            )
        
    usuarios.append(usuario)
    return {
        "mensaje":"Usuario agregado",
        "datos":usuario,
        "status":201
    }
    
@app.put("/v1/usuarios/{id}", tags = ['CRUD Usuarios'])
async def actualizar_usuarios(id:int, usuario:UsuarioBase, usuario_actual:str = Depends(obtener_usuario_actual)):
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
async def eliminar_usuario(id:int, usuario_actual: str = Depends(obtener_usuario_actual)):
    
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
