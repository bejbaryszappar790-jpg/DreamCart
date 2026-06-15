from fastapi import FastAPI
from backend.app.router.user import router as user_router
from backend.app.router.customer import router as customer_router
app = FastAPI()


app.include_router(user_router)
app.include_router(customer_router)