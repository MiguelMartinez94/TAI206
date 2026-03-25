#Importaciones
from fastapi import FastAPI
from app.routers import usuarios, misc
from app.data.db import engine
from app.data import usuario

usuario.Base.metadata.create_all(bind=engine)

#Inicialización del servidor
app = FastAPI(
    title = 'Mi primer API',
    description = 'Esta es mi primera API',
    version = '1.0'
    
)

app.include_router(usuarios.router)
app.include_router(misc.router)




#Modelo de validacion Pydantic


#Seguridad con HTTP Basic


#Endpoints
#@app.get('/', tags=['Inicio'])
#async def holamundo():
#    return {"mensaje":"Hola mundo con FastAPI"}


        

