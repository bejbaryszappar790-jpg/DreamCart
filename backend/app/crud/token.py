from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.models import RefreshToken


async def create_refreshrow(db : AsyncSession, user_id : int, jti : str):
    new_refresh = RefreshToken(user_id = user_id, 
                               jti = jti, 
                               is_revoked = False
                               )
    
    db.add(new_refresh)
    await db.commit()
    await db.refresh(new_refresh)
    return new_refresh



async def update_refresh_status(db : AsyncSession, jti : str):
    query = (
        select(RefreshToken)
        .where(RefreshToken.jti == jti)
    )


    result = await db.execute(query)

    token = result.scalars().first()
    if token is None:
        return None
    
    token.is_revoked = True

    await db.commit()
    await db.refresh(token)
    return token


async def search_refresh(db : AsyncSession, jti : str):
    query = (
        select(RefreshToken)
        .where(RefreshToken.jti == jti)
    )


    result = await db.execute(query)
    return result.scalars().first()