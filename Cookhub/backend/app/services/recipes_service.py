from crud.recipes_repository import RecipesRepository
from crud.ingredients_repository import IngredientsRepository
from models.recipes import Recipes
from models.ingredients import Ingredients


class RecipesFacade:
    def __init__(self, session):
        self.recipes_repo = RecipesRepository(session)
        self.ingredients_repo = IngredientsRepository(session)

    def create_recipe(self, name, user_id):
        recipe = Recipes(name, user_id)
        return self.recipes_repo.add(recipe)

    def add_ingredient(self, name, quantity, price, recipe_id):
        ingredient = Ingredients(name, quantity, price, recipe_id)
        return self.ingredients_repo.add(ingredient)

    def change_price_ingredient(self, ingredient_id, new_price):
        ingredient = self.ingredients_repo.get(ingredient_id)
        ingredient.price = new_price
        self.ingredients_repo.session.commit()

    def change_quantity_ingredient(self, ingredient_id, new_quantity):
        ingredient = self.ingredients_repo.get(ingredient_id)
        ingredient.quantity = new_quantity
        self.ingredients_repo.session.commit()

    def get_cost_recipe(self, recipe_id):
        ingredients_recipe = self.ingredients_repo.get_by_recipe(recipe_id)
        total_cost = 0
        total_cost = sum(ing.price * ing.quantity for ing in ingredients_recipe)
        return total_cost

    def remove_ingredient(self, ingredient_id):
        ingredient = self.ingredients_repo.get(ingredient_id)
        self.ingredients_repo.delete(ingredient)
