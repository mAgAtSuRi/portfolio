from pydantic import BaseModel
from app.schemas.recipes_ingredients import RecipeOut

class InputModel(BaseModel):
    class Config:
        extra = "forbid"


class ShoppingCartCreate(InputModel):
    user_id: int


class ShoppingCartOut(InputModel):
    id: int
    user_id: int

    class Config:
        orm_mode = True
