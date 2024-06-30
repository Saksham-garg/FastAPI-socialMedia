from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "c77b3af00a717df72ac7ea979bd9c6c01154e8d344d3c4018d99ea770046543b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expiry = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expiry})

    access_token = jwt.encode(to_encode,SECRET_KEY,algorithm= ALGORITHM)

    return access_token