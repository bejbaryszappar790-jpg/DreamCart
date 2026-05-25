from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL_ENG = os.getenv("DATABASE_URL_ENGINE")

engine = create_async_engine(DB_URL_ENG)

SessionLocal = sessionmaker(autoflush = False, autocommit = False, bind = engine, class_= AsyncSession)

Base = declarative_base()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
