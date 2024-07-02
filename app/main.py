from fastapi import FastAPI

from .database import engine
from . import models
from .router import users,posts,auth
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(users.usersRouter)
app.include_router(posts.postsRouter)
app.include_router(auth.authrouter)



