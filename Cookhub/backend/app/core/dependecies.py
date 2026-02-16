from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.session import get_db
from app.core.security import verify_token
from jose import ExpiredSignatureError, JWTError
from app.services.users_service import UsersFacade


security = HTTPBearer()


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db=Depends(get_db)
        ):
    facade = UsersFacade(db)
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = facade.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_admin(current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin required")
    return current_user
