from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.db.session import get_db
from app.services.recipes_service import RecipesFacade

router = APIRouter()


# Input
class RecipeCreate(BaseModel):
    name: str
    user_id: int


class IngredientCreate(BaseModel):
    name: str
    quantity: float
    price: int


# Output
class IngredientOut(BaseModel):
    id: int
    name: str
    quantity: float
    price: int

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
    recipe = facade.create_recipe(
        name=recipe.name,
        user_id=recipe.user_id
    )
    return recipe


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
