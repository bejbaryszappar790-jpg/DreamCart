from fastapi import APIRouter, Depends, HTTPException
from backend.app.schemas.Customer_Registration import Cus_Registration_In, Cus_Registration_Out
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database import get_db
from backend.app.crud.customer import search_cus_by_email, register_customer
from backend.app.security.password import verify_password

router = APIRouter(prefix = "customers", 
                    tags = ["customers"],
                    )




@router.post("/register", response_model = Cus_Registration_Out)
async def Create_NewCustomer(cus_in : Cus_Registration_In, db : AsyncSession = Depends(get_db)):
    check_cus = await search_cus_by_email(db = db, cus_email = cus_in.cus_email)
    
    if check_cus:
        raise HTTPException(status_code = 401, detail = "Customer exists!")
    
   
    
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
    
    
    