from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from . import models
# from .database import engine
from .routers import post, user, auth, vote
# from .config import settings


# models.Base.metadata.create_all(bind=engine) 

origin = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "FastAPI is running successfully 🚀"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
