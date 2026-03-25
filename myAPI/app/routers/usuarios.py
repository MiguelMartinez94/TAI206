from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from app.models.usuario import UsuarioBase, UsuarioPatch
from app.data.database import usuarios
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario


router = APIRouter(
    prefix='/v1/usuarios',
    tags=["CRUD Usuarios"]
)


@router.get("/")
async def consultarUsuarios(db:Session=Depends(get_db)):
    consulta_usuarios = db.query(Usuario).all()
    
    return {
        "usuarios": consulta_usuarios
    }
    
    
@router.post("/")
async def agregar_usuarios(usuario:UsuarioBase, db:Session=Depends(get_db)):
    
    nuevo_usuario = Usuario(nombre = usuario.nombre, edad = usuario.edad)
    
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
        
    
    return {
        "mensaje":"Usuario agregado",
        "datos":nuevo_usuario,
        "status":201
    }
    
@router.get("/{id}")
async def obtener_usuarios_id(id:int ,db:Session=Depends(get_db)):
    
    buscar_usuario = db.query(Usuario).all()
    
    for usr in buscar_usuario:
        if usr.id == id:
            
            return {
                "mensake":"Usuario encontrado",
                "usuario":usr
            }
    raise HTTPException(status_code=404, detail="El usuario no se encontró")
    
    


@router.put("/{id}")
async def actualizar_usuario(id:int, usuario:UsuarioBase, db:Session=Depends(get_db)):
    
    buscar_usuario = db.query(Usuario).all()
    
    for usr in buscar_usuario:
        
        if usr.id == id:
            
            usr.nombre = usuario.nombre
            usr.edad = usuario.edad
            
            db.commit()
            db.refresh(usr)
            
        return {
            "status":200,
            "mensaje":"Usuario actualizado correctamente",
            "datos":usr
            
        }
    
    raise HTTPException(status_code=404, detail="El usuario no existe")


@router.patch("/{id}")
async def patch_usuarios(id:int, usuario:UsuarioPatch, db:Session=Depends(get_db)):
    
    buscar_usuarios = db.query(Usuario).all()
    
    for usr in buscar_usuarios:
        if usr.id == id:
            
            usr.nombre = usuario.nombre
            usr.edad = usuario.edad
            
            db.commit()
            db.refresh(usr)
            
        return {
            "status":200,
            "mensaje":"Usuario actualizado correctamente",
            "datos":usr
            
        }
    raise HTTPException(status_code=404, detail="Usuario no encontardo")

"""
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
"""

@router.delete("/{id}")
async def eliminar_usurio(id:int, db:Session=Depends(get_db)):
    
    buscar_usuario = db.query(Usuario).all()
    
    for usr in buscar_usuario:
        
        if usr.id == id:
            
            db.delete(usr)
            db.commit()
            
        return {
            "mensaje":f"Usuario {id} eliminado",
            "status":200
        }