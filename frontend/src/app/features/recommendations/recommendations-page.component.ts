import { ChangeDetectionStrategy, Component, inject, OnInit, PLATFORM_ID, signal } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { RouterLink } from '@angular/router';
import { UserService } from '../../core/services/user.service';
import { NewsCardComponent } from '../../shared/components/news-card/news-card.component';
import { LoadingErrorComponent } from '../../shared/components/loading-error/loading-error.component';
import { NewsBase } from '../../shared/models/article.model';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-recommendations-page',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [NewsCardComponent, LoadingErrorComponent, RouterLink],
  templateUrl: './recommendations-page.component.html',
  styleUrls: ['./recommendations-page.component.scss'],
})
export class RecommendationsPageComponent implements OnInit {
  private readonly userService = inject(UserService);
  private readonly platformId = inject(PLATFORM_ID);

  recommendations = signal<NewsBase[]>([]);
  currentDiversity = signal<number>(0);
  potentialDiversity = signal<number>(0);
  isLoading = signal(true);
  error = signal<string | null>(null);
  totalRead = signal<number>(0);

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.loadRecommendations();
    }
  }

  loadRecommendations(): void {
    this.isLoading.set(true);
    this.error.set(null);

    forkJoin({
      history: this.userService.getHistory(),
      recommendations: this.userService.getRecommendations(10),
    }).subscribe({
      next: ({ history, recommendations }) => {
        this.totalRead.set(history.total_read);
        this.recommendations.set(recommendations.recommendations);
        this.currentDiversity.set(recommendations.current_diversity);
        this.potentialDiversity.set(recommendations.potential_diversity);
        this.isLoading.set(false);
      },
      error: (err) => {
        console.error('Failed to load recommendations:', err);
        this.error.set('Nie udało się załadować rekomendacji.');
        this.isLoading.set(false);
      },
    });
  }

  get diversityPercent(): number {
    return Math.round(this.currentDiversity() * 100);
  }

  get potentialPercent(): number {
    return Math.round(this.potentialDiversity() * 100);
  }

  get diversityGrowth(): number {
    return this.potentialPercent - this.diversityPercent;
  }
}
