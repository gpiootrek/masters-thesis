from pydantic import BaseModel
from typing import Optional


class NewsBase(BaseModel):
    id: int
    title: str
    content: str
    category: str
    sentiment_bielik: Optional[str] = None
    political_bias_bielik: Optional[str] = None
    sentiment_gemma: Optional[str] = None
    political_bias_gemma: Optional[str] = None
    sentiment_gt: Optional[str] = None
    political_bias_gt: Optional[str] = None


class NewsDetail(NewsBase):
    sentiment_explanation_bielik: Optional[str] = None
    political_bias_explanation_bielik: Optional[str] = None
    sentiment_explanation_gemma: Optional[str] = None
    political_bias_explanation_gemma: Optional[str] = None
