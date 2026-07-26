from fastapi import APIRouter
from app.api.endpoints import news, recommendations, user

api_router = APIRouter()

api_router.include_router(news.router, prefix="/news", tags=["News"])
api_router.include_router(recommendations.router,
                          prefix="/news", tags=["Recommendations"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
