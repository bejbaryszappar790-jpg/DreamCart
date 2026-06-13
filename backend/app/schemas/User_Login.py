from pydantic import BaseModel, Field, EmailStr, ConfigDict


class User_Login_Base(BaseModel):
    pass



class User_Login_In(User_Login_Base):
    user_plain_password : str = Field(..., min_length = 6)
    user_email : EmailStr

class User_Login_Out(User_Login_Base):
    access_token : str
    refresh_token : str
    token_type : str
    model_config = ConfigDict(
        from_attributes = True
    )