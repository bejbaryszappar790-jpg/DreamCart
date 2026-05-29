import bcrypt

def get_hashed_password(plain_password):
    bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt()
    
    return bcrypt.hashpw(bytes, salt).decode('utf-8')



def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))