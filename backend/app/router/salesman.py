from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from backend.app.database import get_db
from backend.app.models import User
from backend.app.security.get_user import get_current_salesman
from backend.app.crud.products import get_sale_products
from backend.app.schemas.Sale_Product import Sale_Product_Out


router = APIRouter(
    prefix = "/salesman",
    tags = ["Salesman"]
)


@router.get("sale_products", response_model = list[Sale_Product_Out])
async def show_sale_products(salesman : User = Depends(get_current_salesman), db : AsyncSession = Depends(get_db)):
    try:
        products = await get_sale_products(db = db, sale_id = salesman.sale_id)

        return products
    except SQLAlchemyError:
        raise HTTPException(status_code = 500, detail = "Internal Server Error!")