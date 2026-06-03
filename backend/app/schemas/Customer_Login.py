from pydantic import BaseModel, Field, EmailStr, ConfigDict


class Cus_Login_Base(BaseModel):
    pass



class Cus_Login_In(Cus_Login_Base):
    cus_plain_password : str = Field(..., min_length = 6)
    cus_email : EmailStr

class Cus_Login_Out(Cus_Login_Base):
    access_token : str
    refresh_token : str
    token_type : str
    model_config = ConfigDict(
        from_attributes = True
    )