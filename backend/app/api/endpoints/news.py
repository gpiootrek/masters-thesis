from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.news import NewsBase, NewsDetail
from app.services import news_service

router = APIRouter()


@router.get("/", response_model=List[NewsBase])
def read_all_news(skip: int = 0, limit: int = 20):
    return news_service.get_all(skip, limit)


@router.get("/random-diverse", response_model=List[NewsBase])
def read_random_diverse_news():
    return news_service.get_random_diverse()


@router.get("/category/{category_name}", response_model=List[NewsBase])
def read_news_by_category(category_name: str, skip: int = 0, limit: int = 20):
    return news_service.get_by_category(category_name, skip, limit)


@router.get("/{news_id}", response_model=NewsDetail)
def read_news_by_id(news_id: int):
    news = news_service.get_by_id(news_id)
    if not news:
        raise HTTPException(
            status_code=404, detail="News nie został znaleziony.")
    return news
