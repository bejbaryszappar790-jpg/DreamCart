from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.crud.categories import get_categories
from backend.app.schemas.Category_Page import Category_Page_In, Category_Page_Out
from backend.app.database import get_db
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter(
    prefix = "/categories",
    tags = ["Categories"]
)
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