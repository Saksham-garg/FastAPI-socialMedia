from fastapi import FastAPI, HTTPException, status, Depends
import psycopg2
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor

from .database import engine,get_db
from . import models,schemas,utils
from .router import users,posts
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(users.usersRouter)
app.include_router(posts.postsRouter)


# try:
#     conn = psycopg2.connect(host='localhost', database='fastapi',
#                             user='postgres', password='root4321', cursor_factory=RealDictCursor)

#     cursor = conn.cursor()
#     print("Database connection was successfull.")
# except Exception as error:
#     print(error)


 


