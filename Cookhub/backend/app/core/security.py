from datetime import datetime, timedelta
from jose import jwt, ExpiredSignatureError, JWTError
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORTITHM = "H256"
ACCESS_TOKEN_EXPIRE_MINUTES = 720


def create_access_token(user_id: int, email: str, is_admin: bool):
    expire = datetime.now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"user_id": user_id, "email": email, "is_admin": is_admin, "exp": expire}
    token = jwt.encode((data, SECRET_KEY, ALGORTITHM))
    return token


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORTITHM)
        return payload
    except ExpiredSignatureError:
        print("Token expired")
        return None
    except JWTError as e:
        print(f"Token not valid: {e}")
        return None