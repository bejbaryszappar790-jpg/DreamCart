import jwt
from jwt.exceptions import PyJWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from backend.app.security.token_generating import SECRET_KEY, ALGORITHM

oauth2_cl = OAuth2PasswordBearer(tokenUrl="/user/login")

def decoding_access_token(token : str = Depends(oauth2_cl)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        if payload is None:
            raise HTTPException(status_code = 401, detail = "Token is invalid or expired!")
        user_id = payload.get("sub")

        if user_id is None or not str(user_id).isdigit():
            raise HTTPException(status_code = 401, detail = "Token is invalid or expired!")
        
        if payload.get("token_name") != "access":
            raise HTTPException(status_code = 401, detail = "Token is invalid or expired!")
        
        return int(user_id)
    except (PyJWTError, ValueError, TypeError):
        raise HTTPException(status_code = 401, detail = "Token is invalid or expired!")
    

def decoding_refresh_token(token : str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])

        if payload is None:
            raise HTTPException(status_code = 401, detail = "Token is invalid or expired")
        
        if payload.get("token_name") != "refresh":
            raise HTTPException(status_code = 401, detail = "Token is invalid or expired!")
        
        return payload
    except (PyJWTError, ValueError, TypeError):
        raise HTTPException(status_code = 401, detail = "Token is invalid or expired!")