from fastapi import FastAPI
from app.api import users
from app.api import recipes
from app.db.base import Base
from app.db.session import engine
import app.models

app = FastAPI()

Base.metadata.create_all(engine)
app.include_router(users.router)
app.include_router(recipes.router)