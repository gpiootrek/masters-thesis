import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { NewsBase, NewsDetail } from '../../shared/models/article.model';

@Injectable({ providedIn: 'root' })
export class NewsService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'https://masters-thesis-py05.onrender.com/api/news';

  getAllNews(skip = 0, limit = 20): Observable<NewsBase[]> {
    const params = new HttpParams()
      .set('skip', skip)
      .set('limit', limit);
    return this.http.get<NewsBase[]>(this.apiUrl, { params });
  }

  getRandomDiverse(): Observable<NewsBase[]> {
    return this.http.get<NewsBase[]>(`${this.apiUrl}/random-diverse`);
  }

  getNewsByCategory(categoryName: string, skip = 0, limit = 20): Observable<NewsBase[]> {
    const params = new HttpParams()
      .set('skip', skip)
      .set('limit', limit);
    return this.http.get<NewsBase[]>(
      `${this.apiUrl}/category/${encodeURIComponent(categoryName)}`,
      { params }
    );
  }

  getNewsById(newsId: number): Observable<NewsDetail> {
    return this.http.get<NewsDetail>(`${this.apiUrl}/${newsId}`);
  }

  getRecommendations(newsId: number): Observable<NewsBase[]> {
    return this.http.get<NewsBase[]>(`${this.apiUrl}/${newsId}/recommendations`);
  }
}
