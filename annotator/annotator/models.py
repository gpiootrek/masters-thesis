from django.db import models
from django.utils import timezone


class Dataset(models.Model):
    name = models.CharField(max_length=300)
    csv_filename = models.CharField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

    @property
    def total_count(self):
        return self.articles.count()

    @property
    def annotated_count(self):
        return self.articles.filter(is_annotated=True).count()

    @property
    def progress_percent(self):
        total = self.total_count
        if total == 0:
            return 0
        return round(self.annotated_count / total * 100, 1)


class NewsArticle(models.Model):
    dataset = models.ForeignKey(
        Dataset, on_delete=models.CASCADE,
        related_name='articles', null=True, blank=True
    )
    category = models.CharField(max_length=200)
    text = models.TextField()
    title = models.TextField()
    
    # Klasyfikacje LLM
    sentiment_bielik = models.CharField(max_length=20)
    sentiment_gemma = models.CharField(max_length=20)
    political_bias_bielik = models.CharField(max_length=20)
    political_bias_gemma = models.CharField(max_length=20)
    
    sentiment_bielik_explanation = models.TextField()
    sentiment_gemma_explanation = models.TextField()
    political_bias_bielik_explanation = models.TextField()
    political_bias_gemma_explanation = models.TextField()
    
    sentiment_gt = models.CharField(max_length=20, blank=True, null=True)
    political_bias_gt = models.CharField(max_length=20, blank=True, null=True)
    
    is_annotated = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.category} - {self.id}"
