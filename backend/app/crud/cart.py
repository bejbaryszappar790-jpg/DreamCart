from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased
from sqlalchemy import Row
from backend.app.models import (
    Cart_Item,
    Variant,
    Attribute,
    Stock,
    Parent_Product
    )


async def create_cart(db : AsyncSession, 
                      attributes : dict, 
                      parent_id : int, 
                      sale_id : int, 
                      cus_id : int,
                      quantity : int
                      ) -> Cart_Item | None:
    
    query = (
        select(Variant, Stock)
        .join(Stock, Variant.var_id == Stock.var_id)
        .where(Variant.parent_id == parent_id, Variant.user_id == sale_id)
        )
    
    for key, value in attributes.items():
        att_alias = aliased(Attribute)
        query = (
            query.join(att_alias, Variant.var_id == att_alias.var_id)
            .where(att_alias.att_name == key, att_alias.att_value == value)
        )
    
    var_result = await db.execute(query)
    row = var_result.first()
    if row:
        
        variant, stock = row

        if variant and stock.stock_quantity >= quantity:
            cart_item = Cart_Item(var_id = variant.var_id, 
                                  user_id = cus_id,
                                  cart_quantity = quantity)
            db.add(cart_item)
            await db.commit()
            await db.refresh(cart_item)
            return cart_item
    
    return None




async def get_cart_items(db : AsyncSession, customer_id : int) -> list[Row]:
    query = (
        select(Parent_Product.parent_id,
               Parent_Product.parent_name,
               Cart_Item.cart_id,
               Cart_Item.cart_quantity,
               Cart_Item.user_id,
               Variant.var_id,
               Variant.var_price,
               Variant.var_image_url
            )
        .select_from(Parent_Product)
        .join(Variant, Variant.parent_id == Parent_Product.parent_id)
        .join(Cart_Item, Cart_Item.var_id == Variant.var_id)
        .where(Cart_Item.user_id == customer_id)
    )



    result = await db.execute(query)
    return list(result.all())