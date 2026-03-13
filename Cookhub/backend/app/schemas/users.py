from pydantic import BaseModel, Field


# Input
class InputModel(BaseModel):
    class Config:
        extra = "forbid"


class UserCreate(InputModel):
    username: str
    email: str
    password: str = Field(min_length=3)
    is_admin: bool = Field(default=False)


class EmailUpdate(InputModel):
    new_email: str


class PasswordUpdate(InputModel):
    new_password: str


# Output
class UserOut(BaseModel):
    username: str
    email: str
    id: int
    is_admin: bool

    class Config:
        from_attributes = True
