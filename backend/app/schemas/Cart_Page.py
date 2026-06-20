from pydantic import BaseModel, ConfigDict




class Cart_Page_Out(BaseModel):
    parent_id : int
    parent_name : str
    user_id : int
    cart_id : int
    var_id : int
    var_price : float
    var_image_url : str
    cart_quantity : int
    model_config = ConfigDict(
        from_attributes = True
    )