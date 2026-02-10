from app.crud.ingredients_repository import IngredientsRepository

from app.crud.recipes_repository import RecipesRepository
from app.crud.shopping_carts_repository import ShoppingCartRepository
from app.crud.shopping_cart_item_repository import ShoppingCartItemRepository
from app.crud.users_repository import UsersRepository
from app.models.shopping_carts import ShoppingCarts
from app.models.shopping_cart_items import ShoppingCartItems
from app.models.ingredients import Ingredients


class ShoppingCartsFacade:
    def __init__(self, session):
        self.ingredient_repo = IngredientsRepository(session)
        self.recipe_repo = RecipesRepository(session)
        self.shopping_cart_repo = ShoppingCartRepository(session)
        self.shopping_cart_item_repo = ShoppingCartItemRepository(session)
        self.users_repo = UsersRepository(session)

    def create_shopping_cart(self, user_id):
        user = self.users_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        if user.shopping_carts:
            raise ValueError("User already has a cart")
        shopping_cart = ShoppingCarts(user_id=user_id)
        self.shopping_cart_repo.add(shopping_cart)
        return shopping_cart

    def get_shopping_cart(self, cart_id):
        return self.shopping_cart_repo.get(cart_id)

    def get_shopping_cart_by_user(self, user_id):
        user = self.users_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        cart = self.shopping_cart_repo.get_by_user(user_id)
        if not cart:
            raise ValueError("This user doesn't have a cart")
        return cart

    def get_all_shopping_carts(self):
        return self.shopping_cart_repo.list()

    def add_recipe_to_cart(self, cart_id, recipe_id):
        shopping_cart = self.shopping_cart_repo.get(cart_id)
        if not shopping_cart:
            raise ValueError("Shopping Cart not found")
        recipe = self.recipe_repo.get(recipe_id)
        if not recipe:
            raise ValueError("Recipe not found")
        if recipe.user_id != shopping_cart.user_id:
            raise ValueError("Recipe doesn't belong to the user")

        # ingredients = self.ingredient_repo.get_by_recipe(recipe_id)
        ingredients_added = False
        for ing in recipe.ingredients:
            item = self.shopping_cart_item_repo.get_by_cart_and_ingredient(
                cart_id,
                ing.id
            )

            if item:
                item.quantity += ing.quantity
            else:
                item = ShoppingCartItems(
                    shopping_cart_id=cart_id,
                    ingredient_id=ing.id,
                    recipe_id=recipe.id,
                    quantity=ing.quantity,
                    unit_price=ing.price,
                    checked=False,
                )
                self.shopping_cart_item_repo.add(item)
                ingredients_added = True
        if not ingredients_added:
            raise ValueError("This recipe doesn't have any ingredient")

        self.calculate_cart_price(cart_id)
        return recipe

    def get_recipes_from_cart(self, cart_id):
        shopping_cart = self.shopping_cart_repo.get(cart_id)
        if not shopping_cart:
            raise ValueError("Shopping cart not found")

        # Get all items from cart
        cart_items = self.shopping_cart_item_repo.find_by_shopping_cart(cart_id)
        # Get all recipe_ids (unique)
        recipe_ids = list({item.recipe_id for item in cart_items if item.recipe_id is not None})
        # Get all the recipes based on their ids
        recipes = [self.recipe_repo.get(rid) for rid in recipe_ids]
        return recipes

    def get_all_ingredients_from_cart(self, cart_id):
        shopping_cart = self.shopping_cart_repo.get(cart_id)
        if not shopping_cart:
            raise ValueError("Shopping cart not found")
        cart_items = self.shopping_cart_item_repo.find_by_shopping_cart(cart_id)
        ingredients = [item for item in cart_items if item.ingredient_id is not None]
        return ingredients

    def add_ingredient_to_cart(self, cart_id, name, quantity, unit, price):
        # Check if cart exists
        shopping_cart = self.shopping_cart_repo.get(cart_id)
        if not shopping_cart:
            raise ValueError("Shopping cart not found")

        # Check if ingredient exists in cart
        item = self.ingredient_repo.get_cart_item_by_name(name, cart_id)
        if item:
            item.quantity += quantity
            self.shopping_cart_item_repo.save()
            return item

        # Else create new ingredient for cart
        ingredient = Ingredients(
            name=name,
            quantity=None,
            unit=unit.value,
            price=price,
            recipe_id=None
        )
        ingredient = self.ingredient_repo.add(ingredient)

        # Create ShoppingCartItem for the new ingredient
        item = ShoppingCartItems(
            shopping_cart_id=cart_id,
            ingredient_id=ingredient.id,
            quantity=quantity,
            unit_price=ingredient.price,
            checked=False,
        )
        return self.shopping_cart_item_repo.add(item)

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
