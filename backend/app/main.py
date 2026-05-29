from fastapi import FastAPI
from backend.app.router.customer import router as cus_router

app = FastAPI()


app.include_router(cus_router)
