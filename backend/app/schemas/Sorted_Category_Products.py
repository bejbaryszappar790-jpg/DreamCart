from pydantic import BaseModel


class Sorted_Category_Products_In(BaseModel):
    number_of_passed_rows : int
    category_id : int
    attribute : int