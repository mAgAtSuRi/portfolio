from pydantic import BaseModel, Field
from enum import Enum


# Input
class InputModel(BaseModel):
    class Config:
        extra = "forbid"


class RecipeCreate(InputModel):
    name: str
    user_id: int
    total_price: int | None = None
    description: str | None = None


class UnitEnum(str, Enum):
    g = "g"
    kg = "kg"
    ml = "ml"
    liter = "l"
    piece = "piece"


class IngredientCreate(InputModel):
    name: str
    quantity: float = Field(default=1, gt=0)
    price: int = Field(default=0, ge=0)
    unit: UnitEnum = UnitEnum.g


class IngredientUpdate(InputModel):
    new_price: int


class RecipeUpdate(InputModel):
    name: str | None = None
    total_price: int | None = None
    description: str | None


# Output
class IngredientOut(BaseModel):
    id: int
    name: str
    quantity: float
    price: int
    unit: UnitEnum

    class Config:
        orm_mode = True


class RecipeOut(BaseModel):
    id: int
    name: str
    user_id: int
    description: str | None
    ingredients: list[IngredientOut] = []
    total_price: int | None

    class Config:
        orm_mode = True
