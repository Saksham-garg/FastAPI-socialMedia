from typing import List, Optional
from fastapi import Depends,status,HTTPException,APIRouter
from .. import schemas,models,oauth2
from ..database import get_db
from sqlalchemy.orm import Session

postsRouter = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@postsRouter.get('/',response_model=List[schemas.Post])
async def get_post(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit:int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(current_user)
    return posts
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # return {"data": posts}


@postsRouter.get('/{id}',response_model=schemas.Post)
async def get_post(id: int,db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cannot found with post id {id} in posts")
    return post


@postsRouter.put('/{id}', response_model=schemas.Post)
async def update_post( id: int,post:schemas.PostCreate ,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s,content = %s,published = %s WHERE id = %s returning *""",
    #                (post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_details = post_query.first()
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cannot found with post id {id} in posts")
    
    if post_details.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail="Not authorized to perform requested action.")
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()
    

@postsRouter.post('/',response_model=schemas.Post) 
async def create_post(post: schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    print(post)
    new_post = models.Post(owner_id = current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    return new_post

@postsRouter.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)
    post_details = post.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cannot found with post id {id} in posts")
    
    if post_details.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail="Not authorized to perform requested action.")
    post.delete(synchronize_session=False)
    db.commit()
    return post  