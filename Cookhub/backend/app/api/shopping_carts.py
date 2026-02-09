from fastapi import APIRouter, Depends, HTTPException
from app.db.session import get_db
from app.services.shopping_cart_service import ShoppingCartsFacade
from app.services.recipes_service import RecipesFacade
from app.schemas.shopping_carts import ShoppingCartCreate, ShoppingCartOut,RecipeOut

router = APIRouter()

# Useless as the shopping cart is created automatically
# @router.post("/shopping_cart", response_model=ShoppingCartOut)
# def create_shopping_cart(shopping_cart: ShoppingCartCreate, db=Depends(get_db)):
#     facade = ShoppingCartsFacade(db)
#     try:
#         shopping_cart = facade.create_shopping_cart(user_id=shopping_cart.user_id)
#         return shopping_cart
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))


@router.get("/shopping_carts", response_model=list[ShoppingCartOut])
def get_all_shopping_carts(db=Depends(get_db)):
    return ShoppingCartsFacade(db).get_all_shopping_carts()


@router.post("/shopping_carts/{shopping_cart_id}/recipes/{recipe_id}", response_model=RecipeOut)
def add_recipe_to_cart(shopping_cart_id: int, recipe_id: int, db=Depends(get_db)):
    facade = ShoppingCartsFacade(db)
    try:
        recipe = facade.add_recipe_to_cart(shopping_cart_id, recipe_id)
        return recipe
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
