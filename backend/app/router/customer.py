from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from backend.app.database import get_db
from backend.app.schemas.Create_Cart import Create_Cart_In, Create_Cart_Out
from backend.app.models import User
from backend.app.security.get_user import get_current_customer
from backend.app.crud.cart import create_cart, get_cart_items
from backend.app.schemas.Cart_Page import Cart_Page_Out
from backend.app.schemas.Order import Order_In, Order_Out
from backend.app.crud.orders import make_order, show_order_items_page
from backend.app.schemas.order_item_page import OrderItem_Out
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
                                cus_id = customer.user_id,
                                quantity = input.quantity
                                )
        
        if result is None:
            raise HTTPException(status_code = 404, detail = "Product described does't exists or there is no product like this!")
        
        return result
    except SQLAlchemyError:
            raise HTTPException(status_code = 500, detail = "Internal Server Error!")

@router.get("/cart_page", response_model = list[Cart_Page_Out])
async def open_cart_page(customer : User = Depends(get_current_customer), db : AsyncSession = Depends(get_db)):
    try:
        result = await get_cart_items(db = db, customer_id = customer.user_id)

        return result
    except SQLAlchemyError:
         raise HTTPException(status_code = 500, detail = "Internal Server Error!")
    

@router.post("/order", response_model = Order_Out)
async def create_order(input : Order_In, customer : User = Depends(get_current_customer), db : AsyncSession = Depends(get_db)):
    try:
        result = await make_order(db = db, cart_ids = input.cart_ids, customer_id = customer.user_id)
        
        if result is None:
            raise HTTPException(status_code = 400, detail = "Cart_Items were not found!")
        return result
    except SQLAlchemyError:
        raise HTTPException(status_code = 500, detail = "Internal Server Error!")
    

@router.get("/my_orders", response_model = list[OrderItem_Out])
async def show_order_items(customer : User = Depends(get_current_customer), db: AsyncSession = Depends(get_db)):
    try:
        order_items = await show_order_items_page(db = db, customer_id = customer.user_id)

        return order_items
    except SQLAlchemyError:
        raise HTTPException(status_code = 500, detail = "Internal Server Error!")
