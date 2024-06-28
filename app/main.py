from fastapi import FastAPI, HTTPException, status
import psycopg2
from typing import Optional
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
app = FastAPI()


try:
    conn = psycopg2.connect(host='localhost', database='fastapi',
                            user='postgres', password='root4321', cursor_factory=RealDictCursor)

    cursor = conn.cursor()
    print("Database connection was successfull.")
except Exception as error:
    print(error)


class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None


@app.get('/posts')
async def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get('/posts/{id}')
async def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cannot found with post id {id} in posts")
    return {"post": post}


@app.put('/posts/{id}')
async def update_post(post: Post, id: int):
    cursor.execute("""UPDATE posts SET title = %s,content = %s,published = %s WHERE id = %s returning *""",
                   (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cannot found with post id {id} in posts")
    return {"post": post}


@app.post('/posts')
async def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cannot found with post id {id} in posts")

    return {"data": post}
