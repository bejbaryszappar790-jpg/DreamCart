from pydantic import (
    BaseModel, 
    ConfigDict,
    Field
)

class Product_Table_Out(BaseModel):
    parent_id : int
    parent_name : str = Field(..., min_length = 1)
    des_id : int
    des_price : float
    des_image_url : str = Field(..., min_length = 1)
    
    model_config = ConfigDict(
        from_attributes = True
    )