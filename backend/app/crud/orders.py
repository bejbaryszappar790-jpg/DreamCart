from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from backend.app.models import (
    Variant,
    Cart_Item,
    Parent_Product,
    Order_Item,
    Orders,
    Payment_Status,
)

async def make_order(db : AsyncSession,
              cart_ids : list[int],
              customer_id : int
              ) -> dict | None:
    query = (
        select(
            Cart_Item.cart_id,
            Cart_Item.cart_quantity,
            Cart_Item.var_id,
            Parent_Product.parent_name,
            Variant.var_price
            )
        .select_from(Cart_Item)
        .join(Variant, Cart_Item.var_id == Variant.var_id)
        .join(Parent_Product, Parent_Product.parent_id == Variant.parent_id)
        .where(Cart_Item.cart_id.in_(cart_ids), Cart_Item.user_id == customer_id)
    )

    result = await db.execute(query)
    rows = list(result.all())
    
    if not rows:
        return None
    

    total_amount = 0
    dic = {
        "total_amount" : total_amount,
        "order_items" : []
    }


    for elements in rows:
        total_amount += (elements[4] * elements[1])
        temp_dict = {

            "cart_id" : elements[0],
            "cart_quantity" : elements[1],
            "parent_name" : elements[3],
            "variant_price" : float(elements[4])
        }
        dic["order_items"].append(temp_dict)

    dic["total_amount"] = float(total_amount)


    new_order = Orders(user_id = customer_id, total_amount = total_amount)

    db.add(new_order)

    await db.flush()


    dic["order_id"] = new_order.order_id

    order_items = []
    for cart in rows:
        new_order_item = Order_Item(order_id = new_order.order_id, 
                                    var_id = cart.var_id, 
                                    order_quantity = cart.cart_quantity, 
                                    price_at_purchase = cart.var_price,
                                    cart_id = cart.cart_id
                                    )
        order_items.append(new_order_item)

    
    db.add_all(order_items)
    await db.commit()
    
    return dic



    
async def get_order(db : AsyncSession, order_id : int) -> Orders | None:
    query = (
        select(Orders)
        .where(Orders.order_id == order_id)
    )

    result = await db.execute(query)

    return result.scalars().first()


async def change_order_status(db : AsyncSession, order_id : int, is_failed : bool) -> Orders | None:
    query = (
        select(Orders)
        .where(Orders.order_id == order_id)
        )
    
    
    result = await db.execute(query)

    order = result.scalars().first()

    if order is None:
        return None
        

    sub_query = (
        select(Order_Item.cart_id)
        .join(Orders, Orders.order_id == Order_Item.order_id)
        .where(Orders.order_id == order_id)
    )


    if not is_failed:
        order.payment_status = Payment_Status.SUCCEEDED

        delete_query = (
            delete(Cart_Item)
            .where(
                Cart_Item.cart_id.in_(sub_query),
                Cart_Item.user_id == order.user_id
            )
        )


        await db.execute(delete_query)

    else:
        order.payment_status = Payment_Status.FAILED



    db.add(order)
    await db.commit()

    return order        




async def show_order_items_page(db : AsyncSession, customer_id : int):
    query = (
        select(Order_Item.order_item_id,
               Order_Item.order_quantity,
               Order_Item.price_at_purchase,
               Parent_Product.parent_name,
               Variant.var_image_url
               )
        .select_from(Order_Item)
        .join(Variant, Variant.var_id == Order_Item.var_id)
        .join(Parent_Product, Variant.parent_id == Parent_Product.parent_id)
        .join(Orders, Orders.order_id == Order_Item.order_id)
        .where(Orders.user_id == customer_id)
    )


    result = await db.execute(query)

    return result.all()