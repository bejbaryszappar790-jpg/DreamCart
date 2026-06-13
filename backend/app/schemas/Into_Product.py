from pydantic import BaseModel, ConfigDict


class Image_Url(BaseModel):
    var_image_url : str

    model_config = ConfigDict(
        from_attributes = True
    )

class Into_Product_Out(BaseModel):
    parent_name : str
    images : list[Image_Url]
    start_price : float
    end_price : float
    attributes : dict[str, list[str]]
    sale_id : int
    
    model_config = ConfigDict(
        from_attributes = True
    )
     