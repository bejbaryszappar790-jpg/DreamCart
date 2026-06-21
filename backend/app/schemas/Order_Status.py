from pydantic import BaseModel



class Order_Status_Attributes(BaseModel):
    att_name : str
    att_value : str

class Order_Status_In(BaseModel):
    parent_id : int




class Order_Status_Out(BaseModel):
    parent_name : str
    variant_price : str
    variant_image_url : str
    variant_attributes : list[Order_Status_Attributes]
    payment_status : str