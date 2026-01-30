from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.users_service import UsersFacade
from app.db.session import Session, get_db

facade = UsersFacade(db)
router = APIRouter()


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    facade.create_user(
        username=user.username,
        email=user.email,
        hashed_password=user.password
    )
    return {"status": "user created"}

@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    facade.get_all_user()

# @router.get("/users/{user_id}")
# def get_user(user_id):
#     return {"user": UsersFacade.get_user(user_id)}