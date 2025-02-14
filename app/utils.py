from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")
def hash_password(password: str):
    return pwd_context.hash(password)

def verifyPassword(plain_passowrd,hashed_password):
    return pwd_context.verify(plain_passowrd,hashed_password)