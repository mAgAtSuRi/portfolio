# gère la connexion à la db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine)


def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()
