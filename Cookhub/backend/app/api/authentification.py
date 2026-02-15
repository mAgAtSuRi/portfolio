from fastapi import FastAPI, APIRouter, Depends, HTTPException
from app.db.session import get_db
from app.services.users_service import UsersFacade
from app.schemas.authentification import LoginRequest, LoginResponse
from app.core.security import create_access_token

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db=Depends(get_db)):
    facade = UsersFacade(db)
    user = facade.get_user_by_email(payload.email)
    if not user or not user.verify_password(payload.password):
        raise HTTPException(
            status_code=401,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(user.id, user.email, user.is_admin)
    return LoginResponse(access_token=token, user=user)
