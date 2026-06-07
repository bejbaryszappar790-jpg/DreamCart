from pydantic import BaseModel, Field, ConfigDict


class Category_Page_In(BaseModel):
    number_of_passed_rows : int


class Category_Page_Out(BaseModel):
    category_id : int
    category_name : str = Field(..., min_length = 1)

    model_config = ConfigDict(
        from_attributes = True
    )
    