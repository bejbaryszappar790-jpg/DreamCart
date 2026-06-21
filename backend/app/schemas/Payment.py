from pydantic import BaseModel




class Payment_In(BaseModel):
    cart_ids : list[int]


class Payment_Out(BaseModel):
    stripe_url : str

