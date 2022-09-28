from fastapi import FastAPI
import models
from database import engine
from routers import  user,auth,post,category,like,comment,admin

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router )
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(category.router)
app.include_router(like.router)
app.include_router(comment.router)
app.include_router(admin.router)

@app.get('/')
def root_api():
    return {"message": "Welcome to The Nghia"}





