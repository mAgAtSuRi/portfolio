from crud.ingredients_repository import IngredientsRepository
from crud.recipes_repository import RecipesRepository
from crud.shopping_carts_repository import ShoppingCartRepository
from crud.shopping_cart_item_repository import ShoppingCartItemRepository
from models.shopping_carts import ShoppingCarts
# from models.recipes import Recipes
from models.shopping_cart_items import ShoppingCartItems


class shopping_cart_facade():
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
		
		existing_items = self.shopping_cart_item_repo.get_by_cart_and_ingredient(
			cart_id, recipe_id
		)
		if existing_items:
			raise ValueError("Recipe already in shopping cart")

		ingredients = self.ingredient_repo.get_by_recipe(recipe_id)
		for ing in ingredients:
			item = ShoppingCartItems(
				shopping_cart_id=cart_id,
				ingredient_id=ing.id,
				recipe_id=recipe_id,
				quantity=ing.quantity,
				checked=False
			)
			self.shopping_cart_item_repo.add(item)
			
