from fastapi import FastAPI
from backend.app.router.user import router as user_router

app = FastAPI()


app.include_router(user_router)
