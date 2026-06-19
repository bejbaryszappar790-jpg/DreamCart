

def validate_iin_biin(sale_input : str | None):
    if sale_input is None:
        return None
    
    if sale_input.isdigit():
        return sale_input
    else:
        raise ValueError("IIN or BIIN format is wrong!")