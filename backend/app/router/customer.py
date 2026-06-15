from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database import get_db
from backend.app.schemas.Create_Cart import Create_Cart_In, Create_Cart_Out
from backend.app.models import User
from backend.app.security.get_user import get_current_customer
from backend.app.crud.cart import create_cart
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix = "/customer",
    tags = ["Customer"]
)


@router.post("/add_item", response_model = Create_Cart_Out)
async def create_new_cartitem(input : Create_Cart_In, 
                              customer : User = Depends(get_current_customer), 
                              db : AsyncSession = Depends(get_db)):
    try:
        result = await create_cart(db = db, 
                                attributes = input.attributes, 
                                parent_id = input.parent_id, 
                                sale_id = input.sale_id, 
                                cus_id = customer.user_id
                                )
        
        if result is None:
            raise HTTPException(status_code = 404, detail = "Product described does't exists or there is no product like this!")
        
        return result
    except SQLAlchemyError:
            raise HTTPException(status_code = 500, detail = "Internal Server Error!")

    