from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database import get_db
from backend.app.schemas.User_Homepage import Homepage_In
from backend.app.schemas.Product_Table import Product_Table_Out
from backend.app.crud.products import get_products
from backend.app.crud.categories import get_categories
from backend.app.schemas.Category_Page import Category_Page_In, Category_Page_Out
from backend.app.schemas.Category_Products import Category_Product_In
from backend.app.schemas.Sorted_Category_Products import Sorted_Category_Products_In

router = APIRouter(
    prefix = "/user",
    tags = ["User"]
    )

"""
Так это главная страница нашего маркетплейса. Здесь будет все основные вещи как таблицы товаров, кнопка категорий и поисковик, кнопка 
с листом каким атрибутом сортировать.
"""
@router.get("/homepage", response_model = list[Product_Table_Out])
async def open_homepage(homepage_in : Homepage_In = Depends(), db : AsyncSession = Depends(get_db)):
    result = await get_products(db = db, number_of_passed_rows = homepage_in.number_of_passed_rows)

    if result is None:
        raise HTTPException(status_code = 500, detail = "Internal Server Error!")
    
    return result


"""
Когда пользователь нажимает на кнопку категорий в главной странице тогда открывается страница с таблицей категорий.
"""
@router.get("/categories", response_model = list[Category_Page_Out])
async def open_category_page(category_page_in : Category_Page_In = Depends(), db : AsyncSession = Depends(get_db)):
    categories = await get_categories(db = db, number_of_passed_rows = category_page_in.number_of_passed_rows)
    if categories is None :
        raise HTTPException(status_code = 500, detail = "Internal Server Error!")
    
    return categories
        
    
"""
Этот роутер позволяет увидеть конкретные товары внутри категорий.
"""
@router.get("/categories/products", response_model = list[Product_Table_Out])
async def get_category_products(category_product_in : Category_Product_In = Depends(), db : AsyncSession = Depends(get_db)):
    result = await get_products(db =db, 
                                category_id = category_product_in.category_id, 
                                number_of_passed_rows = category_product_in.number_of_passed_rows
                                )
    if result is None:
        raise HTTPException(status_code = 500, detail = "Internal Server Error!")
    
    return result

"""
Этот роутер возвращает таблицу товаров сортировнному по определнному аттрибуту Например: цена или id
"""
@router.get("categoties/products/sort", response_model = list[Product_Table_Out])
async def get_sorted_category_products(input : Sorted_Category_Products_In = Depends(), 
                                       db : AsyncSession = Depends(get_db)):
    result = await get_products(db =db,
                                category_id = input.category_id,
                                attribute = input.attribute,
                                number_of_passed_rows = input.number_of_passed_rows
                                )
    
    if result is None:
        raise HTTPException(status_code = 500, detail = "Internal Server Error!")
    
    return result

