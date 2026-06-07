from pydantic import BaseModel


class Category_Product_In(BaseModel):
    number_of_passed_rows : int
    category_id : int
    