from pydantic import BaseModel, ConfigDict



class Create_Cart_Base(BaseModel):
    parent_id : int
    sale_id : int
    quantity : int

class Create_Cart_In(Create_Cart_Base):
    attributes : dict
    

    

class Create_Cart_Out(Create_Cart_Base):
    cart_id : int
    var_id : int
    user_id : int
    
    model_config = ConfigDict(
        from_attributes = True
    )