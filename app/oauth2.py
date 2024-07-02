from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas,database,models
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "c77b3af00a717df72ac7ea979bd9c6c01154e8d344d3c4018d99ea770046543b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expiry})

    access_token = jwt.encode(to_encode,SECRET_KEY,algorithm= ALGORITHM)

    return access_token

def verify_access_token(token:str,credentials_error):

    try:
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        id: str = payload.get('user_id')

        if id is None:
            raise credentials_error
        print(id)
        token_data = schemas.TokenPayload(id = id) # Validate Schema of payload 
    except JWTError as e:
        print(e)
        raise credentials_error
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    print(token)
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
