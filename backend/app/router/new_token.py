from fastapi import APIRouter, HTTPException
from backend.app.schemas.new_token import New_Token_In, New_Token_Out
from backend.app.security.decoding_tokens import decoding_refresh_token
from backend.app.security.token_generating import create_AccessToken, create_RefreshToken



router = APIRouter(prefix = "/new_token",
                   tags = ["New_Token"]
                   )

@router.post("/token", response_model = New_Token_Out)
async def create_new_token(input : New_Token_In):
    payload = decoding_refresh_token(token = input.refresh_token)

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
        "token_name" : "refresh"
    }
    

    access_token = create_AccessToken(data = access_payload)
    refresh_token = create_RefreshToken(data = refresh_payload)


    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token,
        "token_type" : "bearer"
    }