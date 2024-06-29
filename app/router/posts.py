from typing import List
from fastapi import Depends,status,HTTPException,APIRouter
from .. import schemas,models
from ..database import get_db
from sqlalchemy.orm import Session

postsRouter = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@postsRouter.get('/posts',response_model=List[schemas.Post])
async def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # return {"data": posts}


@postsRouter.get('/posts/{id}',response_model=schemas.Post)
async def get_post(id: int,db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cannot found with post id {id} in posts")
    return post


@postsRouter.put('/posts/{id}', response_model=schemas.Post)
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
    

@postsRouter.post('/posts',response_model=schemas.Post) 
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

@postsRouter.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
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