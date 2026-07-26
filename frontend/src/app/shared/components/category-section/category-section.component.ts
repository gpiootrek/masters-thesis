import { ChangeDetectionStrategy, Component, ElementRef, input, viewChild } from '@angular/core';
import { Category } from '../../models/article.model';
import { NewsCardComponent } from '../news-card/news-card.component';

@Component({
  selector: 'app-category-section',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [NewsCardComponent],
  templateUrl: './category-section.component.html',
  styleUrls: ['./category-section.component.scss'],
})
export class CategorySectionComponent {
  category = input.required<Category>();
  readArticleIds = input<Set<number>>(new Set());

  carouselRef = viewChild<ElementRef<HTMLDivElement>>('carousel');

  scroll(direction: 'left' | 'right') {
    const el = this.carouselRef()?.nativeElement;
    if (el) {
      const scrollAmount = el.clientWidth * 0.8;
      el.scrollBy({
        left: direction === 'right' ? scrollAmount : -scrollAmount,
        behavior: 'smooth',
      });
    }
  }
}
