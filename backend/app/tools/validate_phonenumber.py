import phonenumbers
from phonenumbers import NumberParseException

def validate_phone_number(cls, phone : str):
    try:
        number = phonenumbers.parse(phone)

        return phonenumbers.format_number(number, phonenumbers.E164)
        
    except(Exception, NumberParseException):
        raise ValueError("Phonenumber doesn't match region phonenumber standard")
        
        