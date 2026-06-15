from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models import (
    Cart_Item,
    Variant,
    Attribute,
    Stock
    )
from sqlalchemy.future import select
from sqlalchemy.orm import aliased

async def create_cart(db : AsyncSession, 
                      attributes : dict, 
                      parent_id : int, 
                      sale_id : int, 
                      cus_id : int
                      ) -> Cart_Item:
    
    query = (
        select(Variant, Stock)
        .join(Stock, Variant.var_id == Stock.var_id)
        .where(Variant.parent_id == parent_id, Variant.user_id == sale_id)
        )
    
    for key, value in attributes.items():
        att_alias = aliased(Attribute, name = "att_alias")
        query = (
            query.join(att_alias, Variant.var_id == att_alias.vat_id)
            .where(att_alias.att_name == key, att_alias.att_value == value)
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