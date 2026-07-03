from pydantic import BaseModel, ConfigDict

class Sale_Product_Out(BaseModel):
    parent_name : str
    parent_id : int
    var_price : float
    var_image_url : str

    model_config = ConfigDict(
        from_attributes = True
    )