from pydantic import BaseModel, ConfigDict

class OrderItem_Out(BaseModel):
    order_item_id : int
    order_quantity : int
    price_at_purchase : float
    parent_name : str
    var_image_url : str

    model_config = ConfigDict(
        from_attributes = True
    )
