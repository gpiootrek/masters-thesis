import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { NewsBase } from '../../../../shared/models/article.model';
import { NewsCardComponent } from '../../../../shared/components/news-card/news-card.component';

@Component({
  selector: 'app-main-section',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [NewsCardComponent],
  templateUrl: './main-section.component.html',
  styleUrls: ['./main-section.component.scss'],
})
export class MainSectionComponent {
  articles = input.required<NewsBase[]>();
  readArticleIds = input<Set<number>>(new Set());
}
