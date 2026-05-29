from pydantic import BaseModel, Field, EmailStr, field_validator
from phonenumbers import NumberParseException
import phonenumbers

class Cus_Registration_Base(BaseModel):
    cus_f_name : str = Field(..., min_length = 1, max_length = 50)
    cus_l_name : str = Field(..., min_length = 1, max_length = 50)
     
class Cus_Registration_In(Cus_Registration_Base):
    
    cus_email : EmailStr
    plain_password : str = Field(..., min_length = 8)
    cus_phone : str
    @field_validator('cus_phone')
    @classmethod
    def validate_phone_number(cls, cus_number : str) -> str:
        try:
            
            res = phonenumbers.parse(cus_number, None)

            return phonenumbers.format_number(res, phonenumbers.PhoneNumberFormat.E164)
        except (Exception, NumberParseException):
            raise ValueError("Phonenumber doesn't match region phonenumber standard")
        

class Cus_Registration_Out(Cus_Registration_Base):
    cus_phone : str
    cus_email : str