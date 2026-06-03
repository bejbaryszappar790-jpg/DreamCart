from fastapi import APIRouter, Depends, HTTPException
from backend.app.schemas.Customer_Registration import Cus_Registration_In, Cus_Registration_Out
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database import get_db
from backend.app.crud.customer import search_cus_by_email, register_customer
from backend.app.security.password import verify_password
from backend.app.schemas.Customer_Login import Cus_Login_In, Cus_Login_Out
from backend.app.security.token_generating import create_AccessToken, create_RefreshToken

router = APIRouter(prefix = "/customers", 
                    tags = ["customers"],
                    )




@router.post("/register", response_model = Cus_Registration_Out)
async def Create_NewCustomer(cus_in : Cus_Registration_In, db : AsyncSession = Depends(get_db)):
    check_cus = await search_cus_by_email(db = db, cus_email = cus_in.cus_email)
    
    if check_cus:
        raise HTTPException(status_code = 400, detail = "Customer exists!")
    
   
    
    new_cus =  await register_customer(db = db, 
                                       cus_f_name = cus_in.cus_f_name, 
                                       cus_l_name = cus_in.cus_l_name, 
                                       cus_email = cus_in.cus_email, 
                                       cus_phone = cus_in.cus_phone, 
                                       cus_plain_password = cus_in.plain_password)
    
    if new_cus:
        return new_cus
    else:
        raise HTTPException(status_code = 500,  detail = "Internal Server Error!")
    
@router.post("/login", response_model = Cus_Login_Out)
async def customer_login(cus_in : Cus_Login_In, db : AsyncSession = Depends(get_db)):
    
    check_cus = await search_cus_by_email(db = db, cus_email = cus_in.cus_email)
    
    if check_cus is None:
        raise HTTPException(status_code = 404, detail = "Email or password is not valid!")
    
    checked_password = verify_password(plain_password = cus_in.cus_plain_password, hashed_password = check_cus.cus_hashed_password)
    if not checked_password:
        raise HTTPException(status_code = 403, detail = "Email or password is not valid!")
    
    access_payload = {
        "sub" : check_cus.cus_id,
        "email" : check_cus.cus_email,
        "role" : "customer",
        "f_name" : check_cus.cus_f_name,
        "l_name" : check_cus.cus_l_name,
        "token_name" : "access"
    }

    refresh_payload = {
        "sub" : check_cus.cus_id,
        "email" : check_cus.cus_email,
        "role" : "customer",
        "f_name" : check_cus.cus_f_name,
        "l_name" : check_cus.cus_l_name,
        "token_name" : "refresh_token"
    }

    access_token = create_AccessToken(data = access_payload)
    refresh_token = create_RefreshToken(data = refresh_payload)

    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token,
        "token_type" : "bearer"
    }