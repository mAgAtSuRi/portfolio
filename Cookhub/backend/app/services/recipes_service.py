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

    def create_recipe(self, name, user_id, total_price, description):
        user = self.users_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        recipe = Recipes(name=name, user_id=user_id, total_price=total_price, description=description)
        self.recipes_repo.add(recipe)
        return recipe

    def add_ingredient(self, name, quantity, unit, price, recipe_id):
        recipe = self.recipes_repo.get(recipe_id)
        if not recipe:
            raise ValueError("Recipe not found")

        ingredient = Ingredients(
            name=name,
            quantity=quantity,
            unit=unit,
            price=price,
            recipe_id=recipe_id
        )
        return self.ingredients_repo.add(ingredient)

    def get_recipe(self, recipe_id):
        return self.recipes_repo.get(recipe_id)

    def get_all_recipes_by_user(self, user_id):
        return self.recipes_repo.find_by_user(user_id)

    def get_all_recipes(self):
        return self.recipes_repo.list()

    def add_description(self, recipe, description):
        recipe.description = description

    def add_total_price(self, recipe, total_price):
        recipe.total_price = total_price

    def update_recipe(self, recipe_id, name, total_price, description):
        recipe = self.recipes_repo.get(recipe_id)
        if not recipe:
            raise ValueError("Recipe not found")
        if name is not None:
            recipe.name = name
        if total_price is not None:
            self.add_total_price(recipe, total_price)
        if description is not None:
            self.add_description(recipe, description)
        self.recipes_repo.save()
        return recipe

    def get_ingredient(self, ingredient_id):
        return self.ingredients_repo.get(ingredient_id)

    def change_price_ingredient(self, recipe_id, ingredient_id, new_price):
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            raise ValueError("Recipe not found")
        ingredient = self.ingredients_repo.get(ingredient_id)
        if not ingredient:
            raise ValueError("Ingredient not found")
        ingredient.price = new_price
        self.ingredients_repo.save()

    def change_quantity_ingredient(self, recipe_id, ingredient_id, new_quantity):
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            raise ValueError("Recipe not found")
        ingredient = self.ingredients_repo.get(ingredient_id)
        if not ingredient:
            raise ValueError('Ingredient not found')
        ingredient.quantity = new_quantity
        self.ingredients_repo.save()

    def get_price_recipe(self, recipe_id):
        ingredients_recipe = self.ingredients_repo.get_by_recipe(recipe_id)
        total_price = 0
        total_price = sum(ing.price * ing.quantity for ing in ingredients_recipe)
        return total_price

    def remove_recipe(self, recipe_id):
        recipe = self.recipes_repo.get(recipe_id)
        if not recipe:
            raise ValueError("Recipe not found")
        self.recipes_repo.delete(recipe)
        return recipe

    def remove_ingredient(self, recipe_id, ingredient_id):
        ingredient = self.ingredients_repo.get(ingredient_id)
        if not ingredient:
            raise ValueError('Ingredient not found')
        if ingredient.recipe_id != recipe_id:
            raise ValueError("Ingredient doesn't belong to this recipe")
        self.ingredients_repo.delete(ingredient)
        return ingredient
