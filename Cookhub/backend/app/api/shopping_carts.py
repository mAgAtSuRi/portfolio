from fastapi import APIRouter, Depends, HTTPException
from app.db.session import get_db
from app.services.shopping_cart_service import ShoppingCartsFacade
from app.services.recipes_service import RecipesFacade
from app.schemas.shopping_carts import (ShoppingCartCreate,
                                        ShoppingCartOut,
                                        IngredientCreate,
                                        ItemUpdate,
                                        ShoppingCartItemOut,
                                        ShoppingCartAggregated,
                                        ShoppingCartFullOut)
from app.schemas.recipes_ingredients import RecipeOut, IngredientOut

router = APIRouter()

# Legacy route: kept for migrating old users who don't have a shopping cart
# New users get a cart automatically on creation
@router.post("/shopping_cart", response_model=ShoppingCartOut)
def create_shopping_cart(shopping_cart: ShoppingCartCreate, db=Depends(get_db)):
    facade = ShoppingCartsFacade(db)
    try:
        shopping_cart = facade.create_shopping_cart(user_id=shopping_cart.user_id)
        return shopping_cart
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/shopping_carts", response_model=list[ShoppingCartOut])
def get_all_shopping_carts(db=Depends(get_db)):
    return ShoppingCartsFacade(db).get_all_shopping_carts()


@router.post("/shopping_cart/{shopping_cart_id}/recipes/{recipe_id}", response_model=RecipeOut)
def add_recipe_to_cart(shopping_cart_id: int, recipe_id: int, db=Depends(get_db)):
    facade = ShoppingCartsFacade(db)
    try:
        recipe = facade.add_recipe_to_cart(shopping_cart_id, recipe_id)
        return RecipeOut.from_orm(recipe)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/users/{user_id}/shopping_cart", response_model=ShoppingCartOut)
def get_cart_by_user(user_id: int, db=Depends(get_db)):
    facade = ShoppingCartsFacade(db)
    try:
        shopping_cart = facade.get_shopping_cart_by_user(user_id=user_id)
        return shopping_cart
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/shopping_cart/{cart_id}/ingredients", response_model=ShoppingCartItemOut)
def add_ingredient_to_shopping_cart(cart_id: int, ingredient: IngredientCreate, db=Depends(get_db)):
    facade = ShoppingCartsFacade(db)
    shopping_cart = facade.get_shopping_cart(cart_id)
    if not shopping_cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    item = facade.add_ingredient_to_cart(
        cart_id,
        ingredient.name,
        ingredient.quantity,
        ingredient.unit,
        ingredient.price
    )
    return ShoppingCartItemOut.from_orm_item(item)


@router.get("/shopping_cart/{cart_id}/recipes", response_model=list[RecipeOut])
def get_all_recipes_from_cart(cart_id: int, db=Depends(get_db)):
    facade = ShoppingCartsFacade(db)
    try:
        recipes = facade.get_recipes_from_cart(cart_id)
        return [RecipeOut.from_orm(recipe) for recipe in recipes]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/shopping_cart/{cart_id}/ingredients", response_model=list[ShoppingCartItemOut])
def get_all_ingredients_from_cart(cart_id: int, db=Depends(get_db)):
    facade = ShoppingCartsFacade(db)
    try:
        items = facade.get_all_ingredients_from_cart(cart_id)
        return [ShoppingCartItemOut.from_orm_item(item) for item in items]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/shopping_cart/{cart_id}/aggregated", response_model=ShoppingCartAggregated)
def get_agregated_ingredients_from_cart(cart_id: int, db=Depends(get_db)):
    facade = ShoppingCartsFacade(db)
    try:
        items = facade.get_aggregated_ingredients_from_cart(cart_id)
        return items
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/shopping_cart/items/{item_id}", response_model=ShoppingCartItemOut)
def update_ingredient_in_cart(item_id: int, payload: ItemUpdate, db=Depends(get_db)):
    facade = ShoppingCartsFacade(db)
    try:
        item = facade.update_cart_item(item_id, payload.quantity, payload.price)
        return ShoppingCartItemOut.from_orm_item(item)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/shopping_cart/items/{item_id}/toggle", response_model=ShoppingCartItemOut)
def toggle_cart_item(item_id: int, db=Depends(get_db)):
    facade = ShoppingCartsFacade(db)
    try:
        item = facade.toggle_item(item_id)
        return ShoppingCartItemOut.from_orm_item(item)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/users/{user_id}/shopping_cart/full", response_model=ShoppingCartFullOut)
def get_full_cart_by_user(user_id: int, db=Depends(get_db)):
    facade = ShoppingCartsFacade(db)
    try:
        cart = facade.get_shopping_cart_by_user(user_id)
        recipes = facade.get_recipes_from_cart(cart.id)
        recipes_out = [RecipeOut.from_orm(recipe) for recipe in recipes]
        ingredients = facade.get_aggregated_ingredients_from_cart(cart.id)

        return ShoppingCartFullOut(
            id=cart.id,
            user_id=cart.user_id,
            recipes=recipes_out,
            ingredients=ingredients
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/shopping_cart/{cart_id}/total_cost")
def get_cart_cost(cart_id: int, db=Depends(get_db)):
    facade = ShoppingCartsFacade(db)
    try:
        total = facade.calculate_cart_price(cart_id)
        return {"total_cost": total / 100,
                "currency": "EUR"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/shopping_cart/{cart_id}/recipes/{recipe_id}")
def delete_recipe_from_cart(cart_id: int, recipe_id: int, db=Depends(get_db)):
    facade = ShoppingCartsFacade(db)
    try:
        recipe = RecipesFacade(db).get_recipe(recipe_id)
        facade.delete_recipe_from_cart(cart_id, recipe_id)
        return {"status": f"Recipe {recipe.name}, id: {recipe_id} deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/shopping_cart/{cart_id}/ingredients/{ingredient_id}")
def delete_ingredient_from_cart(cart_id: int, ingredient_id: int, db=Depends(get_db)):
    facade = ShoppingCartsFacade(db)
    try:
        item = facade.delete_ingredient_from_cart(cart_id, ingredient_id)
        return {"status": f"{item.ingredients.name} deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))