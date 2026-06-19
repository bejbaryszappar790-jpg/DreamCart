import os
from datetime import datetime, timezone, timedelta
import jwt
from jwt.exceptions import PyJWTError
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY_FOR_JWT", "")
ALGORITHM = os.getenv("ALGORITHM_FOR_JWT", "")
ACCES_TIME = os.getenv("ACCESS_TOKEN_TIME", "30")
REFRESH_TIME = os.getenv("REFRESH_TOKEN_TIME", "30")



def create_AccessToken(data : dict):
    try:
        payload = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes= int(ACCES_TIME))
        
        payload["exp"] = expire
        payload["iat"] = datetime.now(timezone.utc)
        
        token = jwt.encode(payload, SECRET_KEY, algorithm= ALGORITHM)
        return token
    except (ValueError, PyJWTError):
        raise HTTPException(status_code = 500, detail = "Server error!")
    

def create_RefreshToken(data : dict):
    try:
        payload = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days = int(REFRESH_TIME))
        
        payload["exp"] = expire
        payload["iat"] = datetime.now(timezone.utc)
        
        token = jwt.encode(payload, SECRET_KEY,  algorithm= ALGORITHM)
        return token
    except (ValueError, PyJWTError):
        raise HTTPException(status_code = 500, detail = "Server error!")