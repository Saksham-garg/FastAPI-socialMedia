from fastapi import Depends, APIRouter, status, HTTPException
from .. import database
from .. import schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

authrouter = APIRouter(
    tags=['Auth']
)


@authrouter.post('/login', status_code=status.HTTP_200_OK, response_model=schemas.LoginToken)
async def login_user(login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == login.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not found")

    comparePassword = utils.verifyPassword(login.password, user.password)
    print(comparePassword)
    if not comparePassword:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Email or Password is incorrect")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    