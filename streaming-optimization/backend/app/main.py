from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.games import router as games_router
from app.routers.offers import router as offers_router
from app.routers.packages import router as packages_router
from app.routers.comparison import router as comparison_router

# FastAPI-Instanz erstellen
app = FastAPI(
    title="Streaming Package Comparator API",
    description="API für Streaming-Pakete und Spiele",
    version="1.0.0",
    root_path="/", 
)

# CORS-Middleware hinzufügen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Erlaube Anfragen vom Frontend
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

# Router registrieren
app.include_router(games_router, prefix="/api/games", tags=["Games"])
app.include_router(offers_router, prefix="/api/offers", tags=["Streaming Offers"])
app.include_router(comparison_router, prefix="/api/comparison")

@app.get("/")
def read_root():
    return {"message": "Willkommen bei der Streaming Package Comparator API!"}