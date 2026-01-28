# test_db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL
from app.db.base import Base
from app.models.users import User
from app.models.recipes import Recipe
from app.models.ingredients import Ingredient
from app.models.shopping_carts import ShoppingCart

# Create engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)

try:
    # 1️⃣ Create user
    user = User(username="tristan_test", email="tristan@test.com", password="secret123")
    session.add(user)
    session.commit()
    print(f"Utilisateur créé : {user.id}, {user.username}")

    # 2️⃣ Create recipe
    recipe = Recipe(name="Pizza Test", user_id=user.id, total_price=1299)
    session.add(recipe)
    session.commit()
    print(f"Recette créée : {recipe.id}, {recipe.name}, user_id={recipe.user_id}")

    # 3️⃣ Create ingredient
    ingredient = Ingredient(name="Fromage", quantity=200, price=499, recipe_id=recipe.id)
    session.add(ingredient)
    session.commit()
    print(f"Ingrédient créé : {ingredient.id}, {ingredient.name}, recette={ingredient.recipe_id}")

    # 4️⃣ Create shopping_cart
    cart = ShoppingCart(user_id=user.id, total_cost=0)
    session.add(cart)
    session.commit()
    print(f"Panier créé : {cart.id}, user_id={cart.user_id}")

finally:
    session.close()
