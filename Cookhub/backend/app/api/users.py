from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.users_service import UsersFacade
from app.db.session import get_db


router = APIRouter()


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_admin: bool


class EmailUpdate(BaseModel):
    new_email: str


class PasswordUpdate(BaseModel):
    new_password: str


def get_users_facade(db=Depends(get_db)):
    return UsersFacade(db)


@router.post("/users")
def create_user(user: UserCreate, db=Depends(get_db)):
    facade = UsersFacade(db)
    try:
        facade.create_user(
            username=user.username,
            email=user.email,
            password=user.password,
            is_admin=user.is_admin
        )
        return {"status": "user created"}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/users")
def list_users(db=Depends(get_db)):
    facade = UsersFacade(db)
    return facade.get_all_user()


@router.get("/users/{user_id}")
def get_user(user_id: int, db=Depends(get_db)):
    facade = UsersFacade(db)
    return {"user": facade.get_user(user_id)}


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db=Depends(get_db)):
    facade = UsersFacade(db)
    try:
        facade.delete_user(user_id)
        return {"status": "user deleted"}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put("/users/{user_id}/email")
def update_email(user_id: int, payload: EmailUpdate, db=Depends(get_db)):
    facade = UsersFacade(db)
    try:
        facade.update_email_user(user_id, payload.new_email)
        return {"status": "user email updated"}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put("/users/{user_id}/password")
def update_password(user_id: int, payload: PasswordUpdate, db=Depends(get_db)):
    facade = UsersFacade(db)
    try:
        facade.update_password_user(user_id, payload.new_password)
        return {"status": "password updated"}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))