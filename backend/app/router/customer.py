from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database import get_db
from backend.app.schemas.Create_Cart import Create_Cart_In, Create_Cart_Out


router = APIRouter(
    prefix = "/customer",
    tags = ["Customer"]
)


@router.post("/add_item", response_model = Create_Cart_Out)
async def create_new_cartitem(input : Create_Cart_Out, customer_id : int, db : AsyncSession):
    