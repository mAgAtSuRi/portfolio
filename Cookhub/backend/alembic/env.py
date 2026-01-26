from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import pool

from alembic import context

from app.db.base import Base
from app.models.user import User
from Cookhub.backend.app.models.recipes import Recipe
from Cookhub.backend.app.models.ingredients import Ingredient
from Cookhub.backend.app.models.shopping_carts import ShoppingCart
from Cookhub.backend.app.models.shopping_cart_items import ShoppingCartItem

from app.core.config import DATABASE_URL

# this is the Alembic Config object
config = context.config

# setup loggers
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object for 'autogenerate'
target_metadata = Base.metadata


# --- offline mode ---
def run_migrations_offline() -> None:
    url = DATABASE_URL  # <-- Use dirctly our db url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# --- online mode ---
def run_migrations_online() -> None:
    # create engine directly with db url
    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# execute selon le mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
