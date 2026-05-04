from sqlalchemy import Column, Integer, String, Float
from database import Base

class Player(Base):
    """
    Modelo de base de datos para jugadores de la NBA

    Este módulo define la estructura de la tabla de jugadores en la base de datos
    utilizando SQLAlchemy.
    """
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    team = Column(String, nullable=False)
    position = Column(String, nullable=False)
    jersey_number = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    nationality = Column(String, nullable=False)
    points_per_game = Column(Float, default=0.0)
    assists_per_game = Column(Float, default=0.0)
    rebounds_per_game = Column(Float, default=0.0)
    image_url = Column(String, nullable=True)