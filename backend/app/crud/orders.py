from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 
from backend.app.models import (
    Variant,
    Cart_Item,
    Parent_Product,
    Order_Item
)

async def make_order(db : AsyncSession,
              cart_ids : list[int],
              customer_id : int
              ) -> dict:
    query = (
        select(
            Cart_Item.cart_id,
            Cart_Item.cart_quantity,
            Parent_Product.parent_name,
            Variant.var_price
            )
        .join(Cart_Item, Cart_Item.var_id == Variant.var_id)
        .join(Parent_Product.parent_id == Variant.parent_id)
        .where(Cart_Item.cart_id.in_(cart_ids), Cart_Item.user_id == customer_id)
    )

    result = await db.execute(query)


    total_amount = 0
    dic = {
        "total_amount" : total_amount,
        "order_items" : []
    }


    for elements in result:
        total_amount += (elements[3] * elements[1])
        temp_dict = {

            "cart_id" : elements[0],
            "cart_quantity" : elements[1],
            "parent_name" : elements[2],
            "variant_price" : elements[3]
        }
        dic["order_items"].append(temp_dict)

    dic["total_amount"] = total_amount

    return dic


async def buy_productbs(db : AsyncSession, cart_ids : list[int], customer_id : int):
    query = (
        select(Cart_Item)
        .where(Cart_Item.cart_id.in_(cart_ids), Cart_Item.user_id == customer_id)
        )
    

    