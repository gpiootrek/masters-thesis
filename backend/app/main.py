from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.router import api_router
import os
import logging

logger = logging.getLogger(__name__)

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


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.method} {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


app.include_router(api_router, prefix="/api")
