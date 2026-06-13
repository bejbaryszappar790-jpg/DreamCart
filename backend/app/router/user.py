from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.schemas.User_Registration import User_Registration_In, User_Registration_Out
from backend.app.crud.categories import get_categories
from backend.app.schemas.Category_Page import Category_Page_In, Category_Page_Out
from backend.app.schemas.Into_Product import Into_Product_Out
from backend.app.crud.user import search_user_by_email, register_user
from backend.app.security.password import verify_password
from backend.app.schemas.User_Login import User_Login_In, User_Login_Out
from backend.app.security.token_generating import create_AccessToken, create_RefreshToken
from backend.app.database import get_db
from backend.app.schemas.Product_Table import Product_Table_Out, Product_Table_In
from sqlalchemy.exc import SQLAlchemyError
from backend.app.crud.products import (
    get_products,
    check_parent,
    open_product
    )

router = APIRouter(
    prefix = "/user",
    tags = ["User"]
    )




@router.post("/register", response_model = User_Registration_Out)
async def Create_Userr(user_in : User_Registration_In, db : AsyncSession = Depends(get_db)):
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
        raise HTTPException(status_code = 500,  detail = "Internal Server Error!")


@router.post("/login", response_model = User_Login_Out)
async def user_login(user_in : User_Login_In, db : AsyncSession = Depends(get_db)):
    
    check_user = await search_user_by_email(db = db, user_email = user_in.user_email)
    
    if check_user is None:
        raise HTTPException(status_code = 404, detail = "Email or password is not valid!")
    
    checked_password = verify_password(
        plain_password = user_in.user_plain_password, 
        hashed_password = check_user.user_hashed_password
        )
    if not checked_password:
        raise HTTPException(status_code = 403, detail = "Email or password is not valid!")
    
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
        "email" : check_user.user_email,
        "role" : check_user.user_role,
        "f_name" : check_user.user_f_name,
        "l_name" : check_user.user_l_name,
        "token_name" : "refresh_token"
    }

    access_token = create_AccessToken(data = access_payload)
    refresh_token = create_RefreshToken(data = refresh_payload)

    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token,
        "token_type" : "bearer"
    }

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



"""
Когда пользователь нажимает на кнопку категорий в главной странице тогда открывается страница с таблицей категорий.
"""
@router.get("/categories", response_model = list[Category_Page_Out])
async def open_category_page(category_page_in : Category_Page_In = Depends(), db : AsyncSession = Depends(get_db)):
    try:
        categories = await get_categories(db = db, number_of_passed_rows = category_page_in.number_of_passed_rows)
        return categories
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

