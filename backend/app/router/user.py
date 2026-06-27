import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.schemas.User_Registration import User_Registration_In, User_Registration_Out
from backend.app.crud.user import search_user_by_email, register_user
from backend.app.security.password import verify_password
from backend.app.schemas.User_Login import User_Login_In, User_Login_Out
from backend.app.security.token_generating import create_AccessToken, create_RefreshToken
from backend.app.database import get_db
from backend.app.crud.token import create_refreshrow



router = APIRouter(
    prefix = "/user",
    tags = ["User"]
    )




@router.post("/register", response_model = User_Registration_Out)
async def Create_User(user_in : User_Registration_In, db : AsyncSession = Depends(get_db)):
    try:
        check_user = await search_user_by_email(db = db, user_email = user_in.user_email)
        
        if check_user:
            raise HTTPException(status_code = 400, detail = "User exists!")
        
    
        
        new_user =  await register_user(db = db, 
                                        user_f_name = user_in.user_f_name, 
                                        user_l_name = user_in.user_l_name, 
                                        user_email = user_in.user_email, 
                                        user_phone = user_in.user_phone, 
                                        user_plain_password = user_in.plain_password,
                                        user_role = user_in.user_role,
                                        sale_biin = user_in.sale_biin,
                                        sale_iin = user_in.sale_iin
                                        )
        
        if new_user:
            return new_user
        else:
            raise HTTPException(status_code = 400,  detail = "IIN or BIIN is Invalid!")
    except SQLAlchemyError:
            raise HTTPException(status_code = 500,  detail = "Internal Server Error!")


@router.post("/login", response_model = User_Login_Out)
async def user_login(user_in : User_Login_In, db : AsyncSession = Depends(get_db)):
    try:
        check_user = await search_user_by_email(db = db, user_email = user_in.user_email)
        
        if check_user is None:
            raise HTTPException(status_code = 401, detail = "Email or password is not valid!")
        
        checked_password = verify_password(
            plain_password = user_in.user_plain_password, 
            hashed_password = check_user.user_hashed_password
            )
        if not checked_password:
            raise HTTPException(status_code = 401, detail = "Email or password is not valid!")
        
        jti = str(uuid.uuid4())

        new_token = create_refreshrow(db = db, user_id = check_user.user_id, jti = jti)
        
        if new_token is None:
            raise HTTPException(status_code = 500, detail = "Internal Server Error!")
        

        access_payload = {
            "sub" : check_user.user_id,
            "email" : check_user.user_email,
            "role" : check_user.user_role,
            "f_name" : check_user.user_f_name,
            "l_name" : check_user.user_l_name,
            "token_name" : "access"
        }

        refresh_payload = {
            "sub" : check_user.user_id,
            "jti" : jti,
            "token_name" : "refresh"
        }

        access_token = create_AccessToken(data = access_payload)
        refresh_token = create_RefreshToken(data = refresh_payload)

        return {
            "access_token" : access_token,
            "refresh_token" : refresh_token,
            "token_type" : "bearer"
        }
    
    except SQLAlchemyError:
        raise HTTPException(status_code = 500,  detail = "Internal Server Error!")



