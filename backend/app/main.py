from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router

app = FastAPI(
    title="News Bubble Breaker API",
    description="API do pracy magisterskiej. Architektura wielowarstwowa.",
    version="1.1.0"
)

# Konfiguracja CORS - niezbędna do połączenia z Angularem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Domyślny port Angulara
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Podpięcie wszystkich endpointów pod globalny prefix /api
app.include_router(api_router, prefix="/api")
