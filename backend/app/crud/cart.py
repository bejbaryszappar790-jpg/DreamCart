from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models import (
    Cart_Item,
    Variant
    )
from sqlalchemy.future import select


async def create_cart(db : AsyncSession, 
                      attributes : dict, 
                      parent_id : int, 
                      sale_id : int, 
                      cus_id : int
                      ):
    
    check_product = (
        select(Variant)
        .where(Variant.parent_id == parent_id, Variant.sale_id == sale_id)
        )
    
    for key, value in attributes.items():
        check_product = (
            check_product.where(Variant.var_id =)
        )