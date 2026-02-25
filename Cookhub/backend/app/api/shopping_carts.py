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
from app.schemas.recipes_ingredients import RecipeOut
from app.core.dependecies import get_current_admin, get_current_user

router = APIRouter()


def check_cart_owner_or_admin(cart, current_user):
    if cart.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You can only change your own cart")


# Legacy route: kept for migrating old users who don't have a shopping cart
# New users get a cart automatically on creation
@router.post("/shopping_cart", response_model=ShoppingCartOut)
def create_shopping_cart(shopping_cart: ShoppingCartCreate,
                         db=Depends(get_db),
                         current_user=Depends(get_current_user)
                         ):
    facade = ShoppingCartsFacade(db)
    try:
        shopping_cart = facade.create_shopping_cart(user_id=current_user.id)
        return shopping_cart
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/shopping_carts", response_model=list[ShoppingCartOut])
def get_all_shopping_carts(db=Depends(get_db), current_admin=Depends(get_current_admin)):
    return ShoppingCartsFacade(db).get_all_shopping_carts()


@router.post("/shopping_cart/{shopping_cart_id}/recipes/{recipe_id}", response_model=RecipeOut)
def add_recipe_to_cart(shopping_cart_id: int,
                       recipe_id: int,
                       db=Depends(get_db),
                       current_user=Depends(get_current_user)
                       ):
    facade = ShoppingCartsFacade(db)
    shopping_cart = facade.get_shopping_cart(shopping_cart_id)
    if not shopping_cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    check_cart_owner_or_admin(shopping_cart, current_user)
    try:
        recipe = facade.add_recipe_to_cart(shopping_cart_id, recipe_id)
        return RecipeOut.from_orm(recipe)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/users/{user_id}/shopping_cart", response_model=ShoppingCartOut)
def get_cart_by_user(user_id: int,
                     db=Depends(get_db),
                     current_user=Depends(get_current_user)
                     ):
    facade = ShoppingCartsFacade(db)
    shopping_cart = facade.get_shopping_cart_by_user(user_id)
    if not shopping_cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    check_cart_owner_or_admin(shopping_cart, current_user)
    return shopping_cart


@router.post("/shopping_cart/{cart_id}/ingredients", response_model=ShoppingCartItemOut)
def add_ingredient_to_shopping_cart(cart_id: int,
                                    ingredient: IngredientCreate,
                                    db=Depends(get_db),
                                    current_user=Depends(get_current_user)
                                    ):
    facade = ShoppingCartsFacade(db)
    shopping_cart = facade.get_shopping_cart(cart_id)
    if not shopping_cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    check_cart_owner_or_admin(shopping_cart, current_user)
    item = facade.add_ingredient_to_cart(
        cart_id,
        ingredient.name,
        ingredient.quantity,
        ingredient.unit,
        ingredient.price
    )
    return ShoppingCartItemOut.from_orm_item(item)


@router.get("/shopping_cart/{cart_id}/recipes", response_model=list[RecipeOut])
def get_all_recipes_from_cart(cart_id: int,
                              db=Depends(get_db),
                              current_user=Depends(get_current_user)
                              ):
    facade = ShoppingCartsFacade(db)
    shopping_cart = facade.get_shopping_cart(cart_id)
    if not shopping_cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    check_cart_owner_or_admin(shopping_cart, current_user)
    try:
        recipes = facade.get_recipes_from_cart(cart_id)
        return [RecipeOut.from_orm(recipe) for recipe in recipes]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/shopping_cart/{cart_id}/ingredients", response_model=list[ShoppingCartItemOut])
def get_all_ingredients_from_cart(cart_id: int,
                                  db=Depends(get_db),
                                  current_user=Depends(get_current_user)
                                  ):
    facade = ShoppingCartsFacade(db)
    shopping_cart = facade.get_shopping_cart(cart_id)
    if not shopping_cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    check_cart_owner_or_admin(shopping_cart, current_user)
    try:
        items = facade.get_all_ingredients_from_cart(cart_id)
        return [ShoppingCartItemOut.from_orm_item(item) for item in items]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/shopping_cart/{cart_id}/aggregated", response_model=ShoppingCartAggregated)
def get_agregated_ingredients_from_cart(cart_id: int,
                                        db=Depends(get_db),
                                        current_user=Depends(get_current_user)
                                        ):
    facade = ShoppingCartsFacade(db)
    shopping_cart = facade.get_shopping_cart(cart_id)
    if not shopping_cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    check_cart_owner_or_admin(shopping_cart, current_user)
    try:
        items = facade.get_aggregated_ingredients_from_cart(cart_id)
        return items
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/shopping_cart/items/{item_id}", response_model=ShoppingCartItemOut)
def update_ingredient_in_cart(item_id: int,
                              payload: ItemUpdate,
                              db=Depends(get_db),
                              current_user=Depends(get_current_user)
                              ):
    facade = ShoppingCartsFacade(db)
    shopping_cart = facade.get_shopping_cart_by_item(item_id)
    if not shopping_cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    check_cart_owner_or_admin(shopping_cart, current_user)
    try:
        item = facade.update_cart_item(item_id, payload.quantity, payload.price)
        return ShoppingCartItemOut.from_orm_item(item)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/shopping_cart/items/{item_id}/toggle", response_model=ShoppingCartItemOut)
def toggle_cart_item(item_id: int,
                     db=Depends(get_db),
                     current_user=Depends(get_current_user)
                     ):
    facade = ShoppingCartsFacade(db)
    shopping_cart = facade.get_shopping_cart_by_item(item_id)
    if not shopping_cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    check_cart_owner_or_admin(shopping_cart, current_user)
    try:
        item = facade.toggle_item(item_id)
        return ShoppingCartItemOut.from_orm_item(item)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/users/{user_id}/shopping_cart/full", response_model=ShoppingCartFullOut)
def get_full_cart_by_user(user_id: int,
                          db=Depends(get_db),
                          current_user=Depends(get_current_user)
                          ):
    facade = ShoppingCartsFacade(db)
    shopping_cart = facade.get_shopping_cart_by_user(user_id)
    if not shopping_cart:
        raise HTTPException(status_code=404, detail=("Shopping cart not found"))
    check_cart_owner_or_admin(shopping_cart, current_user)
    try:
        recipes = facade.get_recipes_from_cart(shopping_cart.id)
        recipes_out = [RecipeOut.from_orm(recipe) for recipe in recipes]
        ingredients = facade.get_aggregated_ingredients_from_cart(shopping_cart.id)

        return ShoppingCartFullOut(
            id=shopping_cart.id,
            user_id=shopping_cart.user_id,
            recipes=recipes_out,
            ingredients=ingredients
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/shopping_cart/{cart_id}/total_cost")
def get_cart_cost(cart_id: int,
                  db=Depends(get_db),
                  current_user=Depends(get_current_user)
                  ):
    facade = ShoppingCartsFacade(db)
    shopping_cart = facade.get_shopping_cart(cart_id)
    if not shopping_cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    check_cart_owner_or_admin(shopping_cart, current_user)
    try:
        total = facade.calculate_cart_price(cart_id)
        return {"total_cost": total / 100,
                "currency": "EUR"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/shopping_cart/{cart_id}/recipes/{recipe_id}")
def delete_recipe_from_cart(cart_id: int,
                            recipe_id: int,
                            db=Depends(get_db),
                            current_user=Depends(get_current_user)
                            ):
    facade = ShoppingCartsFacade(db)
    shopping_cart = facade.get_shopping_cart(cart_id)
    if not shopping_cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    check_cart_owner_or_admin(shopping_cart, current_user)
    try:
        recipe = RecipesFacade(db).get_recipe(recipe_id)
        facade.delete_recipe_from_cart(cart_id, recipe_id)
        return {"status": f"Recipe {recipe.name}, id: {recipe_id} deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/shopping_cart/{cart_id}/items/{item_id}")
def delete_ingredient_from_cart(cart_id: int,
                                item_id: int,
                                db=Depends(get_db),
                                current_user=Depends(get_current_user)
                                ):
    facade = ShoppingCartsFacade(db)
    shopping_cart = facade.get_shopping_cart(cart_id)
    if not shopping_cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    check_cart_owner_or_admin(shopping_cart, current_user)
    try:
        item_name = facade.delete_item_from_cart(cart_id, item_id)
        return {"status": f"{item_name} deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
