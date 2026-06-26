from fastapi import FastAPI
from backend.app.router.user import router as user_router
from backend.app.router.customer import router as customer_router
from backend.app.router.products import router as product_router
from backend.app.router.categories import router as category_router
from backend.app.router.stripe_router import router as stripe_router
app = FastAPI()


app.include_router(user_router)
app.include_router(customer_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(stripe_router)
