import { Routes } from '@angular/router';
import { HomePageComponent } from './features/home/home-page.component';
import { ArticlePageComponent } from './features/article/article-page.component';

export const routes: Routes = [
  { path: '', component: HomePageComponent },
  { path: 'news/:id', component: ArticlePageComponent },
  {
    path: 'recommendations',
    loadComponent: () =>
      import('./features/recommendations/recommendations-page.component').then(
        (m) => m.RecommendationsPageComponent
      ),
  },
  { path: '**', redirectTo: '' },
];
