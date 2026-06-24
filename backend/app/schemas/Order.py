from pydantic import BaseModel



class OrderItems(BaseModel):
    cart_id : int
    cart_quantity : int
    parent_name : str
    variant_price : float
    

class Order_In(BaseModel):
    cart_ids : list[int]


class Order_Out(BaseModel):
    total_amount : float
    order_items : list[OrderItems]
    order_id : int