import uuid
from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.schemas.new_token import New_Token_In, New_Token_Out
from backend.app.security.decoding_tokens import decoding_refresh_token
from backend.app.security.token_generating import create_AccessToken, create_RefreshToken
from backend.app.crud.token import (
    search_refresh, 
    create_refreshrow,
    update_refresh_status
    )



router = APIRouter(prefix = "/new_token",
                   tags = ["New_Token"]
                   )

@router.post("/token", response_model = New_Token_Out)
async def create_new_token(input : New_Token_In, db : AsyncSession):
    payload = decoding_refresh_token(token = input.refresh_token)

    jti : str = payload["jti"]
    user_id : int = payload["sub"]
    
    existing_token = await search_refresh(db = db, jti = jti)


    if existing_token is None:
        raise HTTPException(status_code = 400, detail = "Token is invalid!")
    
    updated_token = await update_refresh_status(db = db, jti = existing_token.jti)
    
    if updated_token is None:
        raise HTTPException(status_code = 400, detail = "Token is invalid")
    


    new_jti = str(uuid.uuid4())
    

    new_refresh_token = await create_refreshrow(db = db, jti = new_jti, user_id = user_id)
    
    if new_refresh_token is None:
        raise HTTPException(status_code = 500, detail = "Internal Server Error!")
    

    
    access_payload = {
            "sub" : payload.get("sub"),
            "email" : payload.get("email"),
            "role" : payload.get("role"),
            "f_name" : payload.get("f_name"),
            "l_name" : payload.get("l_name"),
            "token_name" : "access"
        }

    refresh_payload = {
        "sub" : payload.get("sub"),
        "jti" : new_refresh_token.jti,
        "token_name" : "refresh"
    }
    

    access_token = create_AccessToken(data = access_payload)
    refresh_token = create_RefreshToken(data = refresh_payload)


    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token,
        "token_type" : "bearer"
    }