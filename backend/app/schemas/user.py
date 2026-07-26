from pydantic import BaseModel
from typing import List
from app.schemas.news import NewsBase

class MarkReadRequest(BaseModel):
    user_id: str
    news_id: int

class ReadHistoryResponse(BaseModel):
    user_id: str
    read_article_ids: List[int]
    total_read: int
    diversity_score: float

class RecommendationResponse(BaseModel):
    recommendations: List[NewsBase]
    current_diversity: float
    potential_diversity: float
