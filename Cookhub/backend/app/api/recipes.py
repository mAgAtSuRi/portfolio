from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.db.session import get_db
from app.services.recipes_service import RecipesFacade

router = APIRouter()


class RecipeCreate(BaseModel):
    name: str
    user_id: int


@router.post("/recipes")
def create_recipe(recipe: RecipeCreate, db=Depends(get_db)):
    facade = RecipesFacade(db)
    facade.create_recipe(
        name=recipe.name,
        user_id=recipe.user_id
    )
    return {"status": "recipe created"}

@router.get("/recipes/{user_id}")
def get_all_recipes(user_id: int, db=Depends(get_db)):
    facade = RecipesFacade(db)
    return facade.get_all_recipes(user_id)