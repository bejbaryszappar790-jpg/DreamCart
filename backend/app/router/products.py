from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database import get_db
from backend.app.schemas.Product_Table import Product_Table_Out, Product_Table_In
from backend.app.schemas.Into_Product import Into_Product_Out
from sqlalchemy.exc import SQLAlchemyError
from backend.app.crud.products import (
    get_products,
    check_parent,
    open_product
    )

router = APIRouter(
    prefix = "/products",
    tags = ["Products"]
)
"""
Так этот роутер возвращает таблицы данных. Так как в основе этого роутера лежит динамический КРУД это значит что можно ее
во всех операций где нам нужен результат в виде табиц товаров.
"""
@router.get("/products", response_model = list[Product_Table_Out])
async def open_homepage(input: Product_Table_In = Depends(), db : AsyncSession = Depends(get_db)):
    try:
        result = await get_products(db = db, 
                            number_of_passed_rows = input.number_of_passed_rows, 
                            attribute = input.attribute,
                            user_search = input.user_search,
                            category_id  = input.category_id
                            )
        return result
    except SQLAlchemyError:
        raise HTTPException(status_code = 500, detail = "Internal Server Error!")



@router.get("/products/{parent_id}", response_model = Into_Product_Out)
async def get_product(parent_id : int, db : AsyncSession = Depends(get_db)):
    check = await check_parent(db = db, parent_id = parent_id)

    if check is None:
        raise HTTPException(status_code = 404, detail = "Product does'not exists!")
    

    try:
        result = await open_product(db = db, parent_id = parent_id)
        if result is None:
            raise HTTPException(status_code = 500, detail = "Internal Server Error!")
        return result
    except SQLAlchemyError:
        raise HTTPException(status_code = 500, detail = "Internal Server Error!")
