from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.models import (
     Parent_Product, 
     Product_Description,
     )


async def get_products(db : AsyncSession, 
                       number_of_passed_rows : int, 
                       category_id : int = None, 
                       attribute : str = "id",
                       user_search : str = None
                       ) -> list:
    
    query = (
        select(Parent_Product.parent_name,
               Parent_Product.parent_id,
               Product_Description.des_id,
               Product_Description.des_image_url,
               Product_Description.des_price
               )
        .select_from(Parent_Product)
        .join(Product_Description, Parent_Product.parent_id == Product_Description.parent_id)
        .where(Product_Description.des_order == 1)
    )

    if category_id:
        query = (
            query.where(Parent_Product.category_id == category_id)
        )

    if user_search:
            query = (
                query.where(Parent_Product.parent_name.ilike(f"%{user_search}%"))
            )
        
        
    dict_for_sort = {
        "id" : Parent_Product.parent_id,
        "price" : Product_Description.des_price
    }

    
    order_attribute = dict_for_sort.get(attribute, Parent_Product.parent_id) 

    query = (
        query.order_by(order_attribute)
        .offset(number_of_passed_rows)
        .limit(10)
    )
        
    result = await db.execute(query)
    return result.all()
    

