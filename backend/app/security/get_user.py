from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.security.decoding_tokens import decoding_access_token
from backend.app.crud.user import search_user_by_id
from backend.app.models import User
from backend.app.database import get_db
from sqlalchemy.exc import SQLAlchemyError


async def get_current_customer(cus_id : int = Depends(decoding_access_token),
                               db : AsyncSession = Depends(get_db)) -> User:
    try:
        curr_cus = await search_user_by_id(db = db, user_id = cus_id)
        
        if curr_cus is None:
            raise HTTPException(statuc_code = 404, detail = "User wasn't found!")
        
        if curr_cus.user_role != "customer":
            raise HTTPException(status_code = 403, detail = "Forbidden")
        
        return curr_cus
    except SQLAlchemyError:
        raise HTTPException(status_code = 500, detail = "Internal Server Error!")