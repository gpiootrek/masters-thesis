from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.news import NewsBase
from app.services import recommendation_service

router = APIRouter()


@router.get("/{news_id}/recommendations", response_model=List[NewsBase])
def read_recommendations(news_id: int):
    recommendations = recommendation_service.get_bubble_breaking_recommendations(
        news_id)
    if recommendations is None:
        raise HTTPException(
            status_code=404, detail="News bazowy nie został znaleziony.")
    return recommendations
