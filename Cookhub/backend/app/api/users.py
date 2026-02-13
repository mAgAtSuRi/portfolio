from fastapi import APIRouter, Depends, HTTPException
from app.db.session import get_db
from app.services.users_service import UsersFacade
from app.schemas.users import UserCreate, UserOut, EmailUpdate, PasswordUpdate

router = APIRouter()


@router.post("/users", response_model=UserOut)
def create_user(user: UserCreate, db=Depends(get_db)):
    facade = UsersFacade(db)
    try:
        user = facade.create_user(
            username=user.username,
            email=user.email,
            password=user.password,
            is_admin=user.is_admin
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/users", response_model=list[UserOut])
def list_users(db=Depends(get_db)):
    facade = UsersFacade(db)
    return facade.get_all_user()


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db=Depends(get_db)):
    facade = UsersFacade(db)
    user = facade.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}/email")
def update_email(user_id: int, payload: EmailUpdate, db=Depends(get_db)):
    facade = UsersFacade(db)
    user = facade.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        facade.update_email_user(user_id, payload.new_email)
        return {"status": f"email updated to {payload.new_email}"}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put("/users/{user_id}/password")
def update_password(user_id: int, payload: PasswordUpdate, db=Depends(get_db)):
    facade = UsersFacade(db)
    user = facade.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        facade.update_password_user(user_id, payload.new_password)
        return {"status": "password updated"}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db=Depends(get_db)):
    facade = UsersFacade(db)
    try:
        user = facade.delete_user(user_id)
        return {"status": f"{user.username} with id = {user.id} deleted"}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
