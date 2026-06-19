from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL_ENG = os.getenv(str("DATABASE_URL_ENGINE"))

engine = create_async_engine(str(DB_URL_ENG))

SessionLocal = async_sessionmaker(autoflush = False, autocommit = False, bind = engine, class_= AsyncSession)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as db:
        yield db