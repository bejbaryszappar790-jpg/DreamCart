from pydantic import (
    BaseModel, 
    ConfigDict,
    Field
)


class Product_Table_In(BaseModel):
    number_of_passed_rows : int 
    category_id : int | None
    user_search : str | None
    attribute : str = "id"


class Product_Table_Out(BaseModel):
    parent_id : int
    parent_name : str = Field(..., min_length = 1)
    var_id : int
    var_price : float
    var_image_url : str = Field(..., min_length = 1)
    
    model_config = ConfigDict(
        from_attributes = True
    )