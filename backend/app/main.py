from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
import os
 
app = FastAPI(
    title="News Bubble Breaker API",
    description="API do pracy magisterskiej. Architektura wielowarstwowa.",
    version="1.1.0"
)

frontend_url = os.getenv("FRONTEND_URL", "")
origins = [o.strip() for o in frontend_url.split(",") if o.strip()] if frontend_url else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
