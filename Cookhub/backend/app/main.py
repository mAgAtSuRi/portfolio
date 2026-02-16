from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, recipes, shopping_carts, authentification
from app.db.init_db import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
app.include_router(users.router)
app.include_router(recipes.router)
app.include_router(shopping_carts.router)
app.include_router(authentification.router)
