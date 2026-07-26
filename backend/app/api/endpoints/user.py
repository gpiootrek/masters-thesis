from fastapi import APIRouter, Query
from app.schemas.user import MarkReadRequest, ReadHistoryResponse, RecommendationResponse
from app.services import user_service, recommendation_service

router = APIRouter()

@router.post("/read")
def mark_article_read(request: MarkReadRequest):
    is_new = user_service.mark_article_read(request.user_id, request.news_id)
    return {"status": "ok", "newly_added": is_new}

@router.get("/{user_id}/history", response_model=ReadHistoryResponse)
def get_read_history(user_id: str):
    read_ids = user_service.get_read_history(user_id)
    read_articles = user_service.get_read_articles_data(user_id)
    diversity = recommendation_service.calculate_normalized_diversity(read_articles)
    return {
        "user_id": user_id,
        "read_article_ids": read_ids,
        "total_read": len(read_ids),
        "diversity_score": round(diversity, 6),
    }

@router.get("/{user_id}/recommendations", response_model=RecommendationResponse)
def get_recommendations(user_id: str, count: int = Query(10, ge=1, le=50)):
    read_ids = user_service.get_read_history(user_id)
    result = recommendation_service.get_diversity_recommendations(read_ids, count)
    return result
