from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
db = os.getenv('DB_NAME')

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

try:
    engine = create_engine(DATABASE_URL)
except Exception as e:
    raise RuntimeError(f"No se pudo crear el engine de base de datos: {e}")

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
    session = SessionLocal()
    try:
        yield session
    except SQLAlchemyError as e:
        session.rollback()
        raise RuntimeError(f"Error en la sesión de base de datos: {e}")
    finally:
        session.close()