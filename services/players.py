import os
import uuid
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from psycopg2 import DatabaseError

from models.player import Player
from schemas.player import PlayerCreate, PlayerUpdate
import repositories.player as repo

UPLOAD_DIR = "uploads"
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_all(db: Session) -> list[Player]:
    """
    Obtiene todos los jugadores registrados en la base de datos.
    
    Args:
        db (Session): Sesión de base de datos.
        
    Returns:
        list[Player]: Lista de jugadores registrados.

    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        return repo.get_all(db)
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al obtener los jugadores"
        )

def get_by_id(db: Session, player_id: int) -> Player:
    """
    Obtiene un jugador específico de la base de datos por su ID.
    
    Args:
        db (Session): Sesión de base de datos.
        player_id (int): ID del jugador a obtener.
        
    Returns:
        Player: Jugador encontrado.
        
    Raises:
        HTTPException: Si el jugador no se encuentra (404).
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        return repo.get_by_id(db, player_id)
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al obtener el jugador"
        )

def create(db: Session, data: PlayerCreate) -> Player:
    """
    Agrega un nuevo jugador a la base de datos.
    
    Args:
        db (Session): Sesión de base de datos.
        data (PlayerCreate): Datos del jugador a crear.
        
    Returns:
        Player: Jugador creado.
        
    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        return repo.create(db, data)
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al crear el jugador"
        )

def update(db: Session, player_id: int, data: PlayerUpdate) -> Player:
    """
    Actualiza un jugador específico de la base de datos por su ID.
    
    Args:
        db (Session): Sesión de base de datos.
        player_id (int): ID del jugador a actualizar.
        data (PlayerUpdate): Datos del jugador a actualizar.
        
    Returns:
        Player: Jugador actualizado.
        
    Raises:
        HTTPException: Si el jugador no se encuentra (404).
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        player = get_by_id(db, player_id)
        return repo.update(db, player, data)
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al actualizar el jugador"
        )

def delete(db: Session, player_id: int) -> None:
    """
    Elimina un jugador específico de la base de datos por su ID.
    Tambien elimina la imagen asociada al jugador, si existe.
    
    Args:
        db (Session): Sesión de base de datos.
        player_id (int): ID del jugador a eliminar.
        
    Raises:
        HTTPException: Si el jugador no se encuentra (404).
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        player = get_by_id(db, player_id)
        _delete_image_file(player.image_url)
        repo.delete(db, player)
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al eliminar el jugador"
        )

def upload_image(db: Session, player_id: int, file: UploadFile) -> Player:
    """
    Sube una imagen para un jugador específico de la base de datos por su ID.
    También elimina la imagen anteriormente asociada al jugador, si existe.
    
    Args:
        db (Session): Sesión de base de datos.
        player_id (int): ID del jugador a actualizar.
        file (UploadFile): Imagen a subir.
        
    Returns:
        Player: Jugador actualizado.
        
    Raises:
        HTTPException: Si el tipo de archivo no es permitido (400).
        HTTPException: Si el jugador no se encuentra (404).
        HTTPException: Si no se puede guardar la imagen (500).
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Solo se permiten imágenes JPEG, PNG y WEBP"
        )

    try:
        player = repo.get_by_id(db, player_id)
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al obtener el jugador"
        )

    ext = file.filename.split(".")[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    image_url = f"/uploads/{filename}"

    try:
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        old_image_url = player.image_url
        updated_player = repo.update_image_url(db, player, image_url)
        _delete_image_file(old_image_url)
        return updated_player
    except OSError as e:
        raise HTTPException(
            status_code=500,
            detail=f"No se pudo guardar la imagen: {str(e)}"
        )
    except DatabaseError:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al actualizar la imagen"
        )

def _delete_image_file(image_url: str | None) -> None:
    """
    Elimina un archivo de imagen.
    
    Args:
        image_url (str | None): URL del archivo de imagen a eliminar.
    """
    if image_url:
        file_path = image_url.lstrip("/")
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                pass