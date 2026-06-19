import phonenumbers
from phonenumbers import NumberParseException, PhoneNumberFormat

def validate_phone_number(phone : str):
    try:
        number = phonenumbers.parse(phone)

        return phonenumbers.format_number(number, PhoneNumberFormat.E164)
        
    except NumberParseException:
        raise ValueError("Phonenumber doesn't match region phonenumber standard")
        
        