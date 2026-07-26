import { ChangeDetectionStrategy, Component, inject, OnInit, PLATFORM_ID, signal } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { MainSectionComponent } from './components/main-section/main-section.component';
import { CategorySectionComponent } from '../../shared/components/category-section/category-section.component';
import { LoadingErrorComponent } from '../../shared/components/loading-error/loading-error.component';
import { NewsBase, Category } from '../../shared/models/article.model';
import { NewsService } from '../../core/services/news.service';
import { UserService } from '../../core/services/user.service';
import { getCategoryDisplayName, getCategoryIcon } from '../../shared/utils/category-meta';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-home-page',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [MainSectionComponent, CategorySectionComponent, LoadingErrorComponent],
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
})
export class HomePageComponent implements OnInit {
  private readonly newsService = inject(NewsService);
  private readonly userService = inject(UserService);
  private readonly platformId = inject(PLATFORM_ID);

  readArticleIds = this.userService.readArticleIds;

  mainArticles = signal<NewsBase[]>([]);
  categories = signal<Category[]>([]);
  isLoading = signal(true);
  error = signal<string | null>(null);

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.loadData();
      this.userService.initHistory();
    }
  }

  loadData(): void {
    this.isLoading.set(true);
    this.error.set(null);

    forkJoin({
      diverse: this.newsService.getRandomDiverse(),
      all: this.newsService.getAllNews(0, 200),
    }).subscribe({
      next: ({ diverse, all }) => {
        this.mainArticles.set(diverse);
        this.categories.set(this.buildCategories(all));
        this.isLoading.set(false);
      },
      error: (err) => {
        console.error('Failed to load news data:', err);
        this.error.set(
          'Nie udało się załadować artykułów. Upewnij się, że backend jest uruchomiony.'
        );
        this.isLoading.set(false);
      },
    });
  }

  private buildCategories(articles: NewsBase[]): Category[] {
    const labelSet = new Set(articles.map(n => n.label));
    const categories: Category[] = [];

    for (const label of labelSet) {
      categories.push({
        id: label,
        name: getCategoryDisplayName(label),
        icon: getCategoryIcon(label),
        news: articles.filter(n => n.label === label),
      });
    }

    return categories;
  }
}
