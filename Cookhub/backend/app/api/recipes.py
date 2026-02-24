from fastapi import APIRouter, Depends, HTTPException
from app.db.session import get_db
from app.services.recipes_service import RecipesFacade
from app.schemas.recipes_ingredients import RecipeOut, RecipeCreate, RecipeUpdate, IngredientOut, IngredientCreate, IngredientPriceUpdate, IngredientQuantityUpdate
from app.core.dependecies import get_current_user, get_current_admin

router = APIRouter()


def check_recipe_user_or_admin(recipe, current_user):
    if recipe.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You can only change your own recipes")


# RECIPES
@router.post("/recipes", response_model=RecipeOut)
def create_recipe(recipe: RecipeCreate,
                  db=Depends(get_db),
                  current_user=Depends(get_current_user)
                  ):
    facade = RecipesFacade(db)
    try:
        recipe = facade.create_recipe(
            name=recipe.name,
            user_id=current_user.id,
            total_price=recipe.total_price,
            description=recipe.description
        )
        return RecipeOut.from_orm(recipe)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/recipes", response_model=list[RecipeOut])
def get_all_recipes(db=Depends(get_db), current_admin=Depends(get_current_admin)):
    recipes = RecipesFacade(db).get_all_recipes()
    return [RecipeOut.from_orm(recipe) for recipe in recipes]


@router.get("/users/{user_id}/recipes", response_model=list[RecipeOut])
def get_all_recipes_by_user(user_id: int,
                            db=Depends(get_db),
                            current_user=Depends(get_current_user)
                            ):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You can only see your own recipes")
    recipes = RecipesFacade(db).get_all_recipes_by_user(user_id)
    return [RecipeOut.from_orm(recipe) for recipe in recipes]


@router.get("/recipes/{recipe_id}", response_model=RecipeOut)
def get_recipe(recipe_id: int,
               db=Depends(get_db),
               current_user=Depends(get_current_user)
               ):
    recipe = RecipesFacade(db).get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe doesn't exist")
    check_recipe_user_or_admin(recipe, current_user)
    return RecipeOut.from_orm(recipe)


@router.put("/recipes/{recipe_id}", response_model=RecipeOut)
def update_recipe(recipe_id: int,
                  payload: RecipeUpdate,
                  db=Depends(get_db),
                  current_user=Depends(get_current_user)
                  ):
    facade = RecipesFacade(db)
    recipe = facade.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe doesn't exist")
    check_recipe_user_or_admin(recipe, current_user)
    try:
        updated_recipe = facade.update_recipe(
            recipe_id,
            payload.name,
            payload.total_price,
            payload.description
        )
        return RecipeOut.from_orm(updated_recipe)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int,
                  db=Depends(get_db),
                  current_user=Depends(get_current_user)
                  ):
    facade = RecipesFacade(db)
    recipe = facade.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe doesn't exist")
    check_recipe_user_or_admin(recipe, current_user)
    try:
        recipe_name = facade.remove_recipe(recipe_id)
        return {"status": f"{recipe_name} deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# INGREDIENTS
@router.post("/recipes/{recipe_id}/ingredients", response_model=IngredientOut)
def add_ingredient_to_recipe(ingredient: IngredientCreate,
                             recipe_id: int,
                             db=Depends(get_db),
                             current_user=Depends(get_current_user)
                             ):
    facade = RecipesFacade(db)
    recipe = facade.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    check_recipe_user_or_admin(recipe, current_user)
    ingredient = facade.add_ingredient(
        ingredient.name,
        ingredient.quantity,
        ingredient.unit,
        ingredient.price,
        recipe_id=recipe_id
    )
    return IngredientOut.from_orm(ingredient)


@router.get("/recipes/{recipe_id}/ingredients", response_model=list[IngredientOut])
def get_ingredients_from_recipe(recipe_id: int,
                                db=Depends(get_db),
                                current_user=Depends(get_current_user)
                                ):
    recipe = RecipesFacade(db).get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    check_recipe_user_or_admin(recipe, current_user)
    return [IngredientOut.from_orm(ing) for ing in recipe.ingredients]


@router.put("/recipes/{recipe_id}/ingredients/price/{ingredient_id}", response_model=IngredientOut)
def update_price_ingredient_from_recipe(recipe_id: int,
                                        ingredient_id: int,
                                        payload: IngredientPriceUpdate,
                                        db=Depends(get_db),
                                        current_user=Depends(get_current_user)
                                        ):
    facade = RecipesFacade(db)
    recipe = facade.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe doesn't exist")
    check_recipe_user_or_admin(recipe, current_user)
    try:
        facade.change_price_ingredient(recipe_id, ingredient_id, payload.new_price)
        ingredient = facade.get_ingredient(ingredient_id)
        return IngredientOut.from_orm(ingredient)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/recipes/{recipe_id}/ingredients/quantity/{ingredient_id}", response_model=IngredientOut)
def update_quantity_ingredient_from_recipe(recipe_id: int,
                                           ingredient_id: int,
                                           payload: IngredientQuantityUpdate,
                                           db=Depends(get_db),
                                           current_user=Depends(get_current_user)
                                           ):
    facade = RecipesFacade(db)
    recipe = facade.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe doesn't exist")
    check_recipe_user_or_admin(recipe, current_user)
    try:
        facade.change_quantity_ingredient(recipe_id, ingredient_id, payload.new_quantity)
        ingredient = facade.get_ingredient(ingredient_id)
        return IngredientOut.from_orm(ingredient)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/recipes/{recipe_id}/ingredients/{ingredient_id}")
def delete_ingredient_from_recipe(recipe_id: int,
                                  ingredient_id: int,
                                  db=Depends(get_db),
                                  current_user=Depends(get_current_user)
                                  ):
    facade = RecipesFacade(db)
    recipe = facade.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe doesn't exist")
    check_recipe_user_or_admin(recipe, current_user)
    try:
        ingredient_name = facade.remove_ingredient(recipe_id, ingredient_id)  
        return {"status": f"{ingredient_name} deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
