from pydantic import BaseModel, Field
from typing import Optional

class PlayerBase(BaseModel):
    name: str
    team: str
    position: str
    jersey_number: int
    age: int
    nationality: str
    points_per_game: float = 0.0
    assists_per_game: float = 0.0
    rebounds_per_game: float = 0.0

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    team: Optional[str] = None
    position: Optional[str] = None
    jersey_number: Optional[int] = None
    age: Optional[int] = None
    nationality: Optional[str] = None
    points_per_game: Optional[float] = None
    assists_per_game: Optional[float] = None
    rebounds_per_game: Optional[float] = None

class PlayerResponse(PlayerBase):
    id: int
    image_url: Optional[str] = None

    class Config:
        from_attributes = True