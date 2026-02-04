from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.db.session import get_db
from app.services.recipes_service import RecipesFacade
from enum import Enum

router = APIRouter()


# Input
class RecipeCreate(BaseModel):
    name: str
    user_id: int


class UnitEnum(str, Enum):
    g = "g"
    kg = "kg"
    ml = "ml"
    liter = "l"
    piece = "piece"


class IngredientCreate(BaseModel):
    name: str
    quantity: float = Field(default=1, gt=0)
    price: int = Field(default=0, ge=0)
    unit: UnitEnum = UnitEnum.g


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


# RECIPES
@router.post("/recipes", response_model=RecipeOut)
def create_recipe(recipe: RecipeCreate, db=Depends(get_db)):
    facade = RecipesFacade(db)
    try:
        recipe = facade.create_recipe(
            name=recipe.name,
            user_id=recipe.user_id
        )
        return recipe
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/recipes", response_model=list[RecipeOut])
def get_all_recipes(db=Depends(get_db)):
    return RecipesFacade(db).get_all_recipes()


@router.get("/users/{user_id}/recipes", response_model=list[RecipeOut])
def get_all_recipes_by_user(user_id: int, db=Depends(get_db)):
    return RecipesFacade(db).get_all_recipes_by_user(user_id)


@router.get("/recipes/{recipe_id}", response_model=RecipeOut)
def get_recipe(recipe_id: int, db=Depends(get_db)):
    recipe = RecipesFacade(db).get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe doesn't exist")
    return recipe


# INGREDIENTS
@router.post("/recipes/{recipe_id}/ingredients", response_model=IngredientOut)
def add_ingredient_to_recipe(ingredient: IngredientCreate, recipe_id: int, db=Depends(get_db)):
    facade = RecipesFacade(db)
    recipe = facade.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    ingredient = facade.add_ingredient(
        ingredient.name,
        ingredient.quantity,
        ingredient.price,
        recipe_id=recipe_id
    )
    return ingredient


@router.get("/recipes/{recipe_id}/ingredients", response_model=list[IngredientOut])
def get_ingredients_from_recipe(recipe_id: int, db=Depends(get_db)):
    recipe = RecipesFacade(db).get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe.ingredients


@router.delete("/recipes/{recipe_id}/ingredients/{ingredient_id}")
def delete_ingredient_from_recipe(recipe_id: int, ingredient_id: int, db=Depends(get_db)):
    facade = RecipesFacade(db)
    try:
        ingredient = facade.remove_ingredient(recipe_id, ingredient_id)  
        return {"status": f"{ingredient.name} deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# DELETE /recipes/{id}
# PATCH /recipes/{id}
# DELETE /recipes/{recipe_id}/ingredients/{ingredient_id}
# PATCH /ingredients/{ingredient_id}