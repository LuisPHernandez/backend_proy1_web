from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from database import get_db
from schemas.player import PlayerCreate, PlayerUpdate, PlayerResponse
import services.player as service

router = APIRouter(prefix="/players", tags=["players"])

@router.get(
    "/", 
    response_model=list[PlayerResponse], 
    status_code=200,
    summary="Obtiene todos los jugadores",
    description="Retorna una lista de todos los jugadores registrados en la base de datos"
)
def get_players(db: Session = Depends(get_db)):
    """
    Retorna una lista de todos los jugadores registrados en la base de datos.
    
    Args:
        db (Session): Sesión de base de datos.
        
    Returns:
        list[PlayerResponse]: Lista de jugadores registrados.

    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    return service.get_all(db)

@router.get(
    "/{player_id}", 
    response_model=PlayerResponse, 
    status_code=200,
    summary="Obtiene un jugador por ID",
    description="Retorna un jugador específico de la base de datos"
)
def get_player(player_id: int, db: Session = Depends(get_db)):
    """
    Retorna un jugador específico de la base de datos.
    
    Args:
        player_id (int): ID del jugador a obtener.
        db (Session): Sesión de base de datos.
        
    Returns:
        PlayerResponse: Jugador encontrado.
        
    Raises:
        HTTPException: Si el jugador no se encuentra (404).
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    return service.get_by_id(db, player_id)

@router.post(
    "/", 
    response_model=PlayerResponse, 
    status_code=201,
    summary="Crea un nuevo jugador",
    description="Agrega un nuevo jugador a la base de datos"
)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    """
    Agrega un nuevo jugador a la base de datos.
    
    Args:
        player (PlayerCreate): Datos del jugador a crear.
        db (Session): Sesión de base de datos.
        
    Returns:
        PlayerResponse: Jugador creado.

    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    return service.create(db, player)

@router.put(
    "/{player_id}", 
    response_model=PlayerResponse, 
    status_code=200,
    summary="Obtiene un jugador por ID y lo actualiza",
    description="Obtiene un jugador específico de la base de datos y actualiza sus datos"
)
def update_player(player_id: int, player: PlayerUpdate, db: Session = Depends(get_db)):
    """
    Obtiene un jugador específico de la base de datos y actualiza sus datos.
    
    Args:
        player_id (int): ID del jugador a actualizar.
        player (PlayerUpdate): Datos del jugador a actualizar.
        db (Session): Sesión de base de datos.
        
    Returns:
        PlayerResponse: Jugador actualizado.
        
    Raises:
        HTTPException: Si el jugador no se encuentra (404).
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    return service.update(db, player_id, player)

@router.delete(
    "/{player_id}", 
    status_code=204,
    summary="Obtiene un jugador por ID y lo elimina",
    description="Obtiene un jugador específico de la base de datos y lo elimina"
)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un jugador específico de la base de datos y lo elimina.
    También elimina la imagen asociada al jugador, si existe.
    
    Args:
        player_id (int): ID del jugador a eliminar.
        db (Session): Sesión de base de datos.
        
    Raises:
        HTTPException: Si el jugador no se encuentra (404).
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    service.delete(db, player_id)

@router.post(
    "/{player_id}/image", 
    response_model=PlayerResponse, 
    status_code=200,
    summary="Obtiene un jugador por ID y le asocia una imagen",
    description="Obtiene un jugador específico de la base de datos y le asocia una imagen"
)
def upload_image(player_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Obtiene un jugador específico de la base de datos y le asocia una imagen.
    
    Args:
        player_id (int): ID del jugador a actualizar.
        file (UploadFile): Imagen a subir.
        db (Session): Sesión de base de datos.
        
    Returns:
        PlayerResponse: Jugador actualizado.
        
    Raises:
        HTTPException: Si el tipo de archivo no es permitido (400).
        HTTPException: Si el jugador no se encuentra (404).
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    return service.upload_image(db, player_id, file)