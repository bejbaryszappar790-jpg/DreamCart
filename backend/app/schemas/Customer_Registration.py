from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from backend.app.tools.validate_phonenumber import validate_phone_number

class Cus_Registration_Base(BaseModel):
    cus_f_name : str = Field(..., min_length = 1, max_length = 50)
    cus_l_name : str = Field(..., min_length = 1, max_length = 50)
    cus_email : EmailStr
    cus_phone : str
    @field_validator('cus_phone')
    @staticmethod
    def phone_validation(cus_phone : str):
        result = validate_phone_number(phone = cus_phone)

        return result
        

class Cus_Registration_In(Cus_Registration_Base):
    
    plain_password : str = Field(..., min_length = 8)
        

class Cus_Registration_Out(Cus_Registration_Base):

    
    model_config = ConfigDict(
        from_attributes = True
    )