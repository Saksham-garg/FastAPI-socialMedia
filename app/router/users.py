from fastapi import Depends,status,HTTPException,APIRouter
from .. import schemas,models,utils
from ..database import get_db
from sqlalchemy.orm import Session

usersRouter = APIRouter(
    prefix='/users',
    tags=['Users']
)

@usersRouter.post('/users',status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    try:
        user.password = utils.hash_password(user.password)
        user = models.User(**user.model_dump())


        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User not created")
        
        db.add(user)

        db.commit()
        db.refresh(user)

        return user
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=error)



@usersRouter.get('/users/{id}',response_model=schemas.UserOut)
async def get_user(id: int,db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cannot found with user id {id} in users")
    return user