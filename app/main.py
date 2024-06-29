from fastapi import FastAPI, HTTPException, status, Depends
import psycopg2
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor

from .database import engine,get_db
from . import models,schemas,utils
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# try:
#     conn = psycopg2.connect(host='localhost', database='fastapi',
#                             user='postgres', password='root4321', cursor_factory=RealDictCursor)

#     cursor = conn.cursor()
#     print("Database connection was successfull.")
# except Exception as error:
#     print(error)


@app.get('/posts',response_model=List[schemas.Post])
async def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # return {"data": posts}


@app.get('/posts/{id}',response_model=schemas.Post)
async def get_post(id: int,db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cannot found with post id {id} in posts")
    return post


@app.put('/posts/{id}', response_model=schemas.Post)
async def update_post( id: int,post:schemas.PostCreate ,db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s,content = %s,published = %s WHERE id = %s returning *""",
    #                (post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cannot found with post id {id} in posts")
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()
    

@app.post('/posts',response_model=schemas.Post) 
async def create_post(post: schemas.PostCreate,db: Session = Depends(get_db)):
    print(post)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    return new_post

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,db: Session = Depends(get_db)):
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cannot found with post id {id} in posts")
    post.delete(synchronize_session=False)
    db.commit()
    return post   


@app.post('/users',status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    try:
        user.password = utils.hash(user.password)
        user = models.User(**user.model_dump())


        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User not created")
        
        db.add(user)

        db.commit()
        db.refresh(user)

        return user
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=error)



@app.get('/users/{id}',response_model=schemas.UserOut)
async def get_user(id: int,db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cannot found with user id {id} in users")
    return user