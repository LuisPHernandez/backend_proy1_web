from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
db = os.getenv('DB_NAME')

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Proporciona una sesión de base de datos para una petición.

    Genera una sesión de base de datos y garantiza que
    se cierre correctamente al finalizar su uso.

    Yields:
        Session: Sesión de base de datos de SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        # Asegura que la sesión se cierre al terminar la petición
        db.close()