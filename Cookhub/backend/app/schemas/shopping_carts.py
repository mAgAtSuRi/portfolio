from pydantic import BaseModel, Field, field_validator
from enum import Enum
from app.models.shopping_cart_items import ShoppingCartItems


class InputModel(BaseModel):
    class Config:
        extra = "forbid"


class ShoppingCartCreate(InputModel):
    user_id: int


class UnitEnum(Enum):
    g = "g"
    kg = "kg"
    liter = "l"
    ml = "ml"
    piece = "piece"


class IngredientCreate(InputModel):
    name: str
    quantity: float = Field(default=1, gt=0)
    unit: UnitEnum = UnitEnum.g
    price: float = Field(default=0, ge=0)

    @field_validator("price", mode="before")
    def convert_price_to_cents(cls, value):
        return int(float(value) * 100)


class ShoppingCartOut(InputModel):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class ShoppingCartItemOut(InputModel):
    id: int
    name: str
    quantity: float
    unit: UnitEnum = UnitEnum.g
    price: float
    checked: bool

    @classmethod
    def from_orm_item(cls, item: ShoppingCartItems):
        return cls(
            id=item.id,
            name=item.ingredients.name,
            quantity=item.quantity,   
            unit=item.ingredients.unit,
            price=item.unit_price,
            checked=item.checked,
        )

    @field_validator("price", mode="before")
    def convert_price_to_euros(cls, value):
        if value is None:
            return None
        return value / 100


class IngredientOut(InputModel):
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
