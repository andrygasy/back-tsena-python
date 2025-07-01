from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Définition de la base pour les modèles
Base = declarative_base()

# Dépendance de session pour les routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
