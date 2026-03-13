from pydantic import BaseModel
from app.schemas.users import UserOut

class LoginRequest(BaseModel):
	email: str
	password: str


class LoginResponse(BaseModel):
	access_token: str
	token_type: str = "bearer"
	user: UserOut