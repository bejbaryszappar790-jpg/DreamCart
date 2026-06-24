import os
import stripe
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()


stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

async def get_stripe_url(stripe_amount : int, success_url : str, cancel_url : str, order_id):
    try:
        session = await stripe.checkout.Session.create_async(
            line_items = [
                {
                    'price_data' : {
                        'currency' : 'usd',
                        'product_data' : {
                            'name' : f'Payment of order number: {order_id} for DreamCart',
                        },
                        'unit_amount' : stripe_amount,
                    },
                    'quantity' : 1
                },
            ],
            mode = 'payment',
            success_url = success_url,
            cancel_url = cancel_url,
            metadata = {
                'order_id' : order_id
            }
        )

        return session.url
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))