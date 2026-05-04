from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from models.player import Player
from schemas.player import PlayerCreate, PlayerUpdate

def get_all(db: Session) -> list[Player]:
    """
    Obtiene todos los jugadores registrados en la base de datos.
    
    Args:
        db (Session): Sesión de la base de datos.
    
    Returns:
        list[Player]: Lista de jugadores.
    
    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        return db.query(Player).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")

def get_by_id(db: Session, player_id: int) -> Player:
    """
    Obtiene un jugador específico de la base de datos por su ID.
    
    Args:
        db (Session): Sesión de la base de datos.
        player_id (int): ID del jugador.
    
    Returns:
        Player: Jugador.
    
    Raises:
        HTTPException: Si el jugador no se encuentra (404).
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        player = db.query(Player).filter(Player.id == player_id).first()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")

    if not player:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return player

def create(db: Session, data: PlayerCreate) -> Player:
    """
    Agrega un nuevo jugador a la base de datos.
    
    Args:
        db (Session): Sesión de la base de datos.
        data (PlayerCreate): Datos del jugador.
    
    Returns:
        Player: Jugador creado.
    
    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        player = Player(**data.model_dump())
        db.add(player)
        db.commit()
        db.refresh(player)
        return player
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")

def update(db: Session, player: Player, data: PlayerUpdate) -> Player:
    """
    Actualiza un jugador específico de la base de datos.
    
    Args:
        db (Session): Sesión de la base de datos.
        player (Player): Jugador a actualizar.
        data (PlayerUpdate): Datos del jugador.
    
    Returns:
        Player: Jugador actualizado.
    
    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(player, field, value)
        db.commit()
        db.refresh(player)
        return player
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")

def delete(db: Session, player: Player) -> None:
    """
    Elimina un jugador específico de la base de datos.
    
    Args:
        db (Session): Sesión de la base de datos.
        player (Player): Jugador a eliminar.
    
    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        db.delete(player)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")

def update_image_url(db: Session, player: Player, image_url: str) -> Player:
    """
    Actualiza la URL de la imagen de un jugador específico de la base de datos.
    
    Args:
        db (Session): Sesión de la base de datos.
        player (Player): Jugador a actualizar.
        image_url (str): URL de la imagen.
    
    Returns:
        Player: Jugador actualizado.
    
    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        player.image_url = image_url
        db.commit()
        db.refresh(player)
        return player
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")