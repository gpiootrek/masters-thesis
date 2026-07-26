import { Injectable, inject, PLATFORM_ID, signal } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { ReadHistoryResponse, RecommendationResponse } from '../../shared/models/article.model';

@Injectable({ providedIn: 'root' })
export class UserService {
  private readonly http = inject(HttpClient);
  private readonly platformId = inject(PLATFORM_ID);
  private readonly apiUrl = '/api/user';
  private readonly userIdKey = 'horyzonty_user_id';

  readonly userId = signal<string | null>(null);
  readonly readArticleIds = signal<Set<number>>(new Set());

  constructor() {
    if (isPlatformBrowser(this.platformId)) {
      let uid = localStorage.getItem(this.userIdKey);
      if (!uid) {
        uid = crypto.randomUUID();
        localStorage.setItem(this.userIdKey, uid);
      }
      this.userId.set(uid);
    }
  }

  initHistory(): void {
    if (isPlatformBrowser(this.platformId) && this.userId()) {
      this.getHistory().subscribe(history => {
        this.readArticleIds.set(new Set(history.read_article_ids));
      });
    }
  }

  markArticleRead(newsId: number): Observable<any> {
    const uid = this.userId();
    if (!uid) throw new Error('User ID not set');
    
    return this.http.post(`${this.apiUrl}/read`, { user_id: uid, news_id: newsId }).pipe(
      tap(() => {
        const currentSet = new Set(this.readArticleIds());
        currentSet.add(newsId);
        this.readArticleIds.set(currentSet);
      })
    );
  }

  getHistory(): Observable<ReadHistoryResponse> {
    const uid = this.userId();
    if (!uid) throw new Error('User ID not set');
    
    return this.http.get<ReadHistoryResponse>(`${this.apiUrl}/${uid}/history`);
  }

  getRecommendations(count: number = 10): Observable<RecommendationResponse> {
    const uid = this.userId();
    if (!uid) throw new Error('User ID not set');
    
    return this.http.get<RecommendationResponse>(`${this.apiUrl}/${uid}/recommendations?count=${count}`);
  }

  isArticleRead(newsId: number): boolean {
    return this.readArticleIds().has(newsId);
  }
}
