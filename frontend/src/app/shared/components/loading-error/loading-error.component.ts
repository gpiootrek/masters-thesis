import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';

@Component({
  selector: 'app-loading-error',
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './loading-error.component.html',
  styleUrls: ['./loading-error.component.scss'],
})
export class LoadingErrorComponent {
  isLoading = input.required<boolean>();
  error = input.required<string | null>();
  loadingMessage = input<string>('Ładowanie...');
  retry = output<void>();

  onRetry(): void {
    this.retry.emit();
  }
}
