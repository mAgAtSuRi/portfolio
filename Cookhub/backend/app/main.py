from fastapi import FastAPI
from app.api import users
from app.api import recipes
from app.api import shopping_carts
from app.db.init_db import init_db

app = FastAPI()

init_db()
app.include_router(users.router)
app.include_router(recipes.router)
app.include_router(shopping_carts.router)
