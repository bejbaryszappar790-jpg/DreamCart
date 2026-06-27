import bcrypt

def get_hashed_password(plain_password):
    password_bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt()
    
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')



def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))