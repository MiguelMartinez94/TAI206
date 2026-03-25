from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


#URL de Conexión
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:123456@postgres:5432/DB_miapi")

#Motor de Conexión
engine = create_engine(DATABASE_URL)

#Gestor de sesiones
sessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

#Base declarativa de los modelos
Base = declarative_base()

#Función para el manejo de en session en los request
def get_db():
    db = sessionLocal()
    try:
        
        yield db
    finally:
        db.close()
        
        
