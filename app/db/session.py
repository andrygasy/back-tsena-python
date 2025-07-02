from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://admin:adminpassword@51.38.237.164:6969/mydatabase"


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
