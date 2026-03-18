from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

def verificar_peticion(credentials: HTTPBasicCredentials=Depends(security)):
    usuario_auth= secrets.compare_digest(credentials.username, "admin")
    pass_auth= secrets.compare_digest(credentials.password, "1234")
    
    if not (usuario_auth and pass_auth):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Sácate de aquí, no tienes autorización")

    return credentials.username
