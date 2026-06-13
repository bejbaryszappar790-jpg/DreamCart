from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models import (
    Cart_Item,
    Variant,
    Attribute,
    Stock
    )
from sqlalchemy.future import select


async def create_cart(db : AsyncSession, 
                      attributes : dict, 
                      parent_id : int, 
                      sale_id : int, 
                      cus_id : int
                      ):
    
    query = (
        select(Variant, Stock)
        .join(Stock, Variant.var_id == Stock.var_id)
        .where(Variant.parent_id == parent_id, Variant.user_id == sale_id)
        )
    
    for key, value in attributes.items():
        query = (
            query.join(Attribute, Variant.var_id == Attribute.var_id)
            .where(Attribute.att_name == key, Attribute.att_value == value)
        )
    
    var_result = await db.execute(query)
    var_obj = var_result.first()
    if var_obj:
        
        check_stock = var_obj[1]

        if check_stock and check_stock.stock_quantity > 0:
            cart_item = Cart_Item(var_id = var_obj[0].var_id, user_id = cus_id)
            db.add(cart_item)
            await db.commit()
            await db.refresh(cart_item)
            return cart_item
    
    return None