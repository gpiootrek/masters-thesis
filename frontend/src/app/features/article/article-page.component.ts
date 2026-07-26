import { ChangeDetectionStrategy, Component, inject, OnInit, PLATFORM_ID, signal } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { NewsDetail, NewsBase } from '../../shared/models/article.model';
import { NewsService } from '../../core/services/news.service';
import { UserService } from '../../core/services/user.service';
import { NewsCardComponent } from '../../shared/components/news-card/news-card.component';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-article-page',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [NewsCardComponent, RouterLink],
  templateUrl: './article-page.component.html',
  styleUrls: ['./article-page.component.scss'],
})
export class ArticlePageComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly newsService = inject(NewsService);
  private readonly platformId = inject(PLATFORM_ID);
  private readonly userService = inject(UserService);

  article = signal<NewsDetail | null>(null);
  recommendations = signal<NewsBase[]>([]);
  isLoading = signal(true);
  recommendationsLoading = signal(true);
  error = signal<string | null>(null);

  ngOnInit(): void {
    if (!isPlatformBrowser(this.platformId)) {
      return;
    }

    this.route.params.subscribe(params => {
      const newsId = +params['id'];
      if (newsId) {
        this.loadArticle(newsId);
      }
    });
  }

  private loadArticle(newsId: number): void {
    this.isLoading.set(true);
    this.recommendationsLoading.set(true);
    this.error.set(null);

    forkJoin({
      article: this.newsService.getNewsById(newsId),
      recommendations: this.newsService.getRecommendations(newsId),
    }).subscribe({
      next: ({ article, recommendations }) => {
        this.article.set(article);
        this.isLoading.set(false);
        this.recommendations.set(recommendations);
        this.recommendationsLoading.set(false);
        this.userService.markArticleRead(newsId).subscribe();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      },
      error: (err) => {
        console.error('Failed to load article:', err);
        this.error.set('Nie udało się załadować artykułu.');
        this.isLoading.set(false);
        this.recommendationsLoading.set(false);
      },
    });
  }
}
