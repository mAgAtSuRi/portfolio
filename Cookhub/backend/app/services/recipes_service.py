from app.crud.recipes_repository import RecipesRepository
from app.crud.ingredients_repository import IngredientsRepository
from app.crud.users_repository import UsersRepository
from app.models.recipes import Recipes
from app.models.ingredients import Ingredients


class RecipesFacade:
    def __init__(self, session):
        self.recipes_repo = RecipesRepository(session)
        self.ingredients_repo = IngredientsRepository(session)
        self.users_repo = UsersRepository(session)

    def create_recipe(self, name, user_id):
        user = self.users_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        recipe = Recipes(name=name, user_id=user_id)
        self.recipes_repo.add(recipe)
        return recipe

    def add_ingredient(self, name, quantity, price, recipe_id):
        recipe = self.recipes_repo.get(recipe_id)
        if not recipe:
            raise ValueError("Recipe not found")

        ingredient = Ingredients(
            name=name,
            quantity=quantity,
            price=price,
            recipe_id=recipe_id
        )
        return self.ingredients_repo.add(ingredient)

    def add_description(self, recipe_id, description):
        recipe = self.recipes_repo.get(recipe_id)
        if not recipe:
            raise ValueError("Recipe not found")
        recipe.description = description
        self.recipes_repo.save()

    def get_recipe(self, recipe_id):
        return self.recipes_repo.get(recipe_id)

    def get_all_recipes_by_user(self, user_id):
        return self.recipes_repo.find_by_user(user_id)

    def get_all_recipes(self):
        return self.recipes_repo.list()

    def get_ingredient(self, ingredient_id):
        return self.ingredients_repo.get(ingredient_id)

    def change_price_ingredient(self, ingredient_id, new_price):
        ingredient = self.ingredients_repo.get(ingredient_id)
        if not ingredient:
            raise ValueError('Ingredient not found')
        ingredient.price = new_price
        self.ingredients_repo.save()

    def change_quantity_ingredient(self, ingredient_id, new_quantity):
        ingredient = self.ingredients_repo.get(ingredient_id)
        if not ingredient:
            raise ValueError('Ingredient not found')
        ingredient.quantity = new_quantity
        self.ingredients_repo.save()

    def get_cost_recipe(self, recipe_id):
        ingredients_recipe = self.ingredients_repo.get_by_recipe(recipe_id)
        total_cost = 0
        total_cost = sum(ing.price * ing.quantity for ing in ingredients_recipe)
        return total_cost

    def remove_ingredient(self, ingredient_id, recipe_id):
        ingredient = self.ingredients_repo.get(ingredient_id)
        if not ingredient:
            raise ValueError('Ingredient not found')
        if ingredient.recipe_id != recipe_id:
            raise ValueError("Ingredient doesn't belong to this recipe")
        self.ingredients_repo.delete(ingredient)
        return ingredient
