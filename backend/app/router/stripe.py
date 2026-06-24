import os
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import stripe
from dotenv import load_dotenv
from backend.app.database import get_db
from backend.app.schemas.Stripe_URL import Stripe_Url_Out
from backend.app.tools.stripe import get_stripe_url
from backend.app.security.get_user import get_current_customer
from backend.app.models import User
from backend.app.crud.orders import get_order


load_dotenv()

stripe_secret_key = os.getenv("STRIPE_WEBHOOK_SECRET")
router = APIRouter(prefix = "/stripe",
                   tags = ["Stripe"]
                )







@router.post("/orders/{order_id}/pay", response_model = Stripe_Url_Out)
async def pay(order_id : int, customer : User = Depends(get_current_customer), db : AsyncSession = Depends(get_db)):
    try:
        existing_order = await get_order(db = db, order_id = order_id)
        
        if existing_order is None:
            raise HTTPException(status_code = 500, detail = "Internal Server Error!")

        if existing_order.user_id != customer.user_id:
            raise HTTPException(status_code = 403, detail = "Forbidden!")
        
        stripe_amount = int(existing_order.total_amount * 100)
        success_url = "http://localhost:8000/docs"
        cancel_url = "http://localhost:8000/docs"

        stripe_url = await get_stripe_url(stripe_amount = stripe_amount, 
                                      success_url = success_url, 
                                      cancel_url = cancel_url,
                                      order_id = existing_order.order_id
                                      )
        if stripe_url is None:
            raise HTTPException(status_code = 404, detail = "Order was not found!")
        
        return Stripe_Url_Out(stripe_url = stripe_url)
    except SQLAlchemyError:
        raise HTTPException(status_code = 500, detail = "Internal Server Error!")  
    


@router.post("/webhook", response_model = Response)
async def check_webhoook(request : Request, db : AsyncSession = Depends(get_db)):
    sig_header = request.headers.get("stripe-signature")


    payload = await request.body()
    stripe.construct_event(payload, sig_header, stripe_secret_key)

    order_id  = payload.get("metadata", {}).get("order_id")