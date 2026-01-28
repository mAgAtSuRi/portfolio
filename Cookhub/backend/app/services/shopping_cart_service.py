from crud.ingredients_repository import IngredientsRepository
from crud.recipes_repository import RecipesRepository
from crud.shopping_carts_repository import ShoppingCartRepository
from crud.shopping_cart_item_repository import ShoppingCartItemRepository
from models.shopping_carts import ShoppingCarts

# from models.recipes import Recipes
from models.shopping_cart_items import ShoppingCartItems


class ShoppingCartsFacade:
    def __init__(self, session):
        self.ingredient_repo = IngredientsRepository(session)
        self.recipe_repo = RecipesRepository(session)
        self.shopping_cart_repo = ShoppingCartRepository(session)
        self.shopping_cart_item_repo = ShoppingCartItemRepository(session)

    def create_shopping_cart(self, user_id):
        shopping_cart = ShoppingCarts(user_id)
        self.shopping_cart_repo.add(shopping_cart)

    def add_recipe_to_cart(self, cart_id, recipe_id):
        recipe = self.recipe_repo.get(recipe_id)
        if not recipe:
            raise ValueError("Recipe not found")

        ingredients = self.ingredient_repo.get_by_recipe(recipe_id)

        for ing in ingredients:
            item = self.shopping_cart_item_repo.get_by_cart_and_ingredient(
                cart_id, ing.id
            )

            if item:
                item.quantity += ing.quantity
            else:
                item = ShoppingCartItems(
                    shopping_cart_id=cart_id,
                    ingredient_id=ing.id,
                    recipe_id=recipe_id,
                    quantity=ing.quantity,
                    unit_price=ing.price,
                    checked=False,
                )
                self.shopping_cart_item_repo.add(item)

        self.calculate_cart_price(cart_id)

    def add_ingredient_to_cart(self, ingredient_id, cart_id):
        ingredient = self.ingredient_repo.get(ingredient_id)

        item = self.shopping_cart_item_repo.get_by_cart_and_ingredient(
            cart_id, ingredient_id
        )
        if item:
            item.quantity += ingredient.quantity
        else:
            item = ShoppingCartItems(
                shopping_cart_id=cart_id,
                ingredient_id=ingredient.id,
                quantity=ingredient.quantity,
                unit_price=ingredient.price,
                checked=False,
            )
            self.shopping_cart_item_repo.add(item)

    def update_ingredient(self, cart_id, ingredient_id, quantity, price):
        cart_item = self.shopping_cart_item_repo.get_by_cart_and_ingredient(
            cart_id, ingredient_id
        )
        if not cart_item:
            raise ValueError("Ingredient not found")
        cart_item.quantity = quantity
        cart_item.unit_price = price

    def calculate_cart_price(self, cart_id):
        cart = self.shopping_cart_repo.get(cart_id)
        items = self.shopping_cart_item_repo.find_by_shopping_cart(cart_id)
        total = 0
        for item in items:
            if item.checked is False:
                total += item.quantity * item.unit_price
        cart.total_cost = total

    def toggle_item(self, cart_item_id):
        item = self.shopping_cart_item_repo.get(cart_item_id)
        if not item:
            raise ValueError("Item not found")
        item.checked = not item.checked
        self.calculate_cart_price(item.shopping_cart_id)

    def delete_ingredient_from_cart(self, cart_id, ingredient_id):
        item = self.shopping_cart_item_repo.get_by_cart_and_ingredient(
            cart_id, ingredient_id
        )
        if item:
            self.shopping_cart_item_repo.delete(item)
        self.calculate_cart_price(cart_id)

    def delete_recipe_from_cart(self, cart_id, recipe_id):
        items = self.shopping_cart_item_repo.find_by_cart_and_recipe(cart_id, recipe_id)
        for item in items:
            self.shopping_cart_item_repo.delete(item)
        self.calculate_cart_price(cart_id)
