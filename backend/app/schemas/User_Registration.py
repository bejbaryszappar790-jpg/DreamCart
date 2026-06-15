from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from backend.app.tools.validate_phonenumber import validate_phone_number

class User_Registration_Base(BaseModel):
    user_f_name : str = Field(..., min_length = 1, max_length = 50)
    user_l_name : str = Field(..., min_length = 1, max_length = 50)
    user_email : EmailStr
    user_phone : str
    user_role : str = Field(..., min_length = 8, max_length = 8)
    @field_validator('user_phone')
    @staticmethod
    def phone_validation(user_phone : str):
        result = validate_phone_number(phone = user_phone)

        return result
        

class User_Registration_In(User_Registration_Base):
    sale_iin : int | None
    sale_biin : int | None
    plain_password : str = Field(..., min_length = 8)
        

class User_Registration_Out(User_Registration_Base):

    
    model_config = ConfigDict(
        from_attributes = True
    )