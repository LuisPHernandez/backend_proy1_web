from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import engine
from models.player import Player
from routers.players import router as players_router

# Crear las tablas en la base de datos
Player.metadata.create_all(bind=engine)

# Inicialización de la aplicación FastAPI
app = FastAPI(title="NBA Players API")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar el directorio de archivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Incluir los routers
app.include_router(players_router)