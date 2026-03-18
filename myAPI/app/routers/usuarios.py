from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from app.models.usuario import UsuarioBase
from app.data.database import usuarios
from app.security.auth import verificar_peticion


router = APIRouter(
    prefix='/v1/usuarios',
    tags=["CRUD Usuarios"]
)

    
@router.get("/")
async def consultarUsuarios():
    return usuarios
    
@router.post("/")
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
    
@router.put("/{id}")
async def actualizar_usuarios(id:int, usuario:UsuarioBase):
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
    
    
@router.delete("/{id}")
async def eliminar_usuario(id:int, usuario_auth:str = Depends(verificar_peticion)):
    
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
