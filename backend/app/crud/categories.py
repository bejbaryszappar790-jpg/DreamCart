from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.models import Category

async def get_categories(db : AsyncSession, number_of_passed_rows : int):
    query = select(Category).distinct().offset(number_of_passed_rows).limit(10)

    result = await db.execute(query)

    return result.scalars().all()
