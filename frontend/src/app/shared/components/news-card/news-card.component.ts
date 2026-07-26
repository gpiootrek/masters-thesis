import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { RouterLink } from '@angular/router';
import { NewsBase } from '../../models/article.model';

@Component({
  selector: 'app-news-card',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [RouterLink],
  templateUrl: './news-card.component.html',
  styleUrls: ['./news-card.component.scss'],
})
export class NewsCardComponent {
  article = input.required<NewsBase>();
  categoryName = input<string>('');
  isLarge = input<boolean>(false);
  isRead = input<boolean>(false);
}
