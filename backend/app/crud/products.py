from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.models import (
     Parent_Product, 
     Variant,
     Salesman,
     Attribute
    )

"""
Функция-помощник что бы проверять существует ли определнный родительский товар/продукт.
"""
async def check_parent(db : AsyncSession, parent_id : int):
    query = (select(Parent_Product)
            .where(Parent_Product.parent_id == parent_id) 
            )
    result = await db.execute(query)
    return result.first()



"""
Динамически КРУД который зависимости от данных возвращает товары по определенным запросам либо категориям либо же сортированным
по определенным аттрибутам.
"""
async def get_products(db : AsyncSession, 
                       number_of_passed_rows : int, 
                       category_id : int = None, 
                       attribute : str = "id",
                       user_search : str = None
                       ) -> list:
    
    query = (
        select(Parent_Product.parent_name,
               Parent_Product.parent_id,
               Variant.var_id,
               Variant.var_image_url,
               Variant.var_price
               )
        .select_from(Parent_Product)
        .join(Variant, Parent_Product.parent_id == Variant.parent_id)
        .where(Variant.var_order == 1)
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
        "price" : Variant.var_price
    }

    
    order_attribute = dict_for_sort.get(attribute, Parent_Product.parent_id) 

    query = (
        query.order_by(order_attribute)
        .offset(number_of_passed_rows)
        .limit(10)
    )
        
    result = await db.execute(query)
    return result.all()
    


async def open_product(db : AsyncSession, parent_id : int) -> dict:
    query = (
        select(Parent_Product.parent_name,
            Variant.var_image_url,
            Variant.var_price,
            Attribute.att_name,
            Attribute.att_value
        )
        .select_from(Parent_Product)
        .join(Variant, Parent_Product.parent_id == Variant.parent_id)
        .join(Attribute, Variant.var_id == Attribute.var_id)
        .where(Parent_Product.parent_id == parent_id)
        .distinct()
    )
    
    result = await db.execute(query)
    rows = result.all()
    if not rows:
        return None
    

    product = {
        "parent_name" : rows[0].parent_name,
        "images" : [],
        "var_price" : float(rows[0].var_price),
        "attributes" : {}
    }

    images = set()
    
    attributes = {}

    for row in rows:
        if row.att_name not in attributes:
            attributes[row.att_name] = set()
        
        attributes[row.att_name].add(row.att_value)


    for att_name in attributes.keys():
        attributes[att_name] = list(attributes[att_name]) 

    product["attributes"] = attributes

    for row in rows:
        images.add(row.var_image_url)


    for image in images:
        product["images"].append(
            {
            "var_image_url" : image
            }
        )
        

    return product