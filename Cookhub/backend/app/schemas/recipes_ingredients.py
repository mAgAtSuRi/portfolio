from pydantic import BaseModel, Field, field_validator
from enum import Enum


# Input
class InputModel(BaseModel):
    class Config:
        extra = "forbid"


class RecipeCreate(InputModel):
    name: str
    user_id: int
    total_price: float | None = None
    description: str | None = None

    @field_validator("total_price", mode="before")
    def convert_price_to_cents(cls, value):
        if value is None:
            return None
        return int(float(value) * 100)


class UnitEnum(str, Enum):
    g = "g"
    kg = "kg"
    ml = "ml"
    liter = "l"
    piece = "piece"


class IngredientCreate(InputModel):
    name: str
    quantity: float = Field(default=1, gt=0)
    unit: UnitEnum = UnitEnum.g
    price: float = Field(default=0, ge=0)

    @field_validator("price", mode="before")
    def convert_price_to_cents(cls, value):
        return int(float(value) * 100)


class IngredientPriceUpdate(InputModel):
    new_price: float

    @field_validator("new_price", mode="before")
    def convert_price_to_cents(cls, value):
        return int(float(value) * 100)


class IngredientQuantityUpdate(InputModel):
    new_quantity: float


class RecipeUpdate(InputModel):
    name: str | None = None
    total_price: float | None = None
    description: str | None = None

    @field_validator("total_price", mode="before")
    def convert_price_to_cents(cls, value):
        if value is None:
            return None
        return int(value * 100)


# Output
class IngredientOut(BaseModel):
    id: int
    name: str
    quantity: float
    unit: UnitEnum
    price: float

    class Config:
        orm_mode = True

    @field_validator("price", mode="before")
    def convert_price_to_euros(cls, value):
        if value is None:
            return None
        return value / 100


class RecipeOut(BaseModel):
    id: int
    name: str
    user_id: int
    description: str | None
    ingredients: list[IngredientOut] = []
    total_price: float | None

    class Config:
        orm_mode = True

    @field_validator("total_price", mode="before")
    def convert_price_to_euros(cls, value):
        if value is None:
            return None
        return value / 100
