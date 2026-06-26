import csv
import io
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import NewsArticle, Dataset


def datasets_list(request):
    """Main page: overview of all datasets with statistics."""
    datasets = Dataset.objects.all().order_by('-created_at')

    POLITICAL_BIAS_CHOICES = ['lewicowe', 'centrowe', 'prawicowe']
    SENTIMENT_CHOICES = ['negatywny', 'neutralny', 'pozytywny']

    datasets_data = []
    for ds in datasets:
        articles = ds.articles.all()
        annotated_articles = articles.filter(is_annotated=True)

        # Build template-friendly table: list of rows, each with label + cells
        combo_rows = []
        for bias in POLITICAL_BIAS_CHOICES:
            cells = []
            for sent in SENTIMENT_CHOICES:
                count = annotated_articles.filter(
                    political_bias_gt=bias, sentiment_gt=sent
                ).count()
                cells.append(count)
            combo_rows.append({'label': bias, 'cells': cells})

        datasets_data.append({
            'dataset': ds,
            'combo_rows': combo_rows,
        })

    context = {
        'datasets_data': datasets_data,
        'sentiment_choices': SENTIMENT_CHOICES,
    }
    return render(request, 'datasets.html', context)



def upload_csv(request):
    if request.method == "POST" and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        csv_filename = csv_file.name
        decoded_file = csv_file.read().decode('utf-8-sig')
        io_string = io.StringIO(decoded_file)
        
        first_line = decoded_file.splitlines()[0]
        delimiter = ';' if ';' in first_line else ','
        
        reader = csv.DictReader(io_string, delimiter=delimiter)

        # Create a new dataset for this upload
        dataset_name = csv_filename.rsplit('.', 1)[0] if '.' in csv_filename else csv_filename
        dataset = Dataset.objects.create(
            name=dataset_name,
            csv_filename=csv_filename,
        )
        
        count = 0
        for row in reader:
            text_val = row.get('content', '').strip()
            
            if not text_val:
                continue
                
            if not NewsArticle.objects.filter(text=text_val, dataset=dataset).exists():
                NewsArticle.objects.create(
                    dataset=dataset,
                    category=row.get('label', ''),
                    text=text_val,
                    title=row.get('title', ''),
                    sentiment_bielik=row.get('sentiment_bielik', ''),
                    sentiment_gemma=row.get('sentiment_gemma', ''),
                    political_bias_bielik=row.get('political_bias_bielik', ''),
                    political_bias_gemma=row.get('political_bias_gemma', ''),
                    sentiment_bielik_explanation=row.get('sentiment_explanation_bielik', ''),
                    sentiment_gemma_explanation=row.get('sentiment_explanation_gemma', ''),
                    political_bias_bielik_explanation=row.get('political_bias_explanation_bielik', ''),
                    political_bias_gemma_explanation=row.get('political_bias_explanation_gemma', ''),
                )
                count += 1

        if count == 0:
            # No articles imported, remove the empty dataset
            dataset.delete()

        return redirect('datasets_list')
    return render(request, 'upload.html')


def annotate(request, dataset_id=None):
    # Determine which dataset to work with
    dataset = None
    if dataset_id:
        dataset = get_object_or_404(Dataset, id=dataset_id)
        qs = NewsArticle.objects.filter(dataset=dataset)
    else:
        qs = NewsArticle.objects.all()

    if request.method == "POST":
        article_id = request.POST.get('article_id')
        article = NewsArticle.objects.get(id=article_id)

        article.sentiment_gt = request.POST.get('sentiment')
        article.political_bias_gt = request.POST.get('political_bias')
        article.is_annotated = True
        article.save()

        if dataset_id:
            return redirect('annotate_dataset', dataset_id=dataset_id)
        return redirect('annotate')

    article = qs.filter(is_annotated=False).first()

    total_count = qs.count()
    annotated_count = qs.filter(is_annotated=True).count()

    if not article:
        return render(request, 'annotate_done.html', {
            'dataset': dataset,
            'total': total_count,
            'annotated': annotated_count,
        })

    context = {
        "article": article,
        "total": total_count,
        "current": annotated_count + 1,
        "dataset": dataset,
    }

    return render(request, "annotate.html", context)


def export_csv(request, dataset_id=None):
    if dataset_id:
        dataset = get_object_or_404(Dataset, id=dataset_id)
        articles = NewsArticle.objects.filter(dataset=dataset)
        filename = f"{dataset.name}_annotated.csv"
    else:
        articles = NewsArticle.objects.all()
        filename = "annotated_articles_gt.csv"

    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow([
        'id', 'category', 'title', 'content',
        'sentiment_bielik', 'sentiment_gemma',
        'political_bias_bielik', 'political_bias_gemma',
        'sentiment_explanation_bielik', 'sentiment_explanation_gemma',
        'political_bias_explanation_bielik', 'political_bias_explanation_gemma',
        'sentiment_gt', 'political_bias_gt'])

    for article in articles:
        writer.writerow([
            article.id, article.category, article.title, article.text,
            article.sentiment_bielik, article.sentiment_gemma,
            article.political_bias_bielik, article.political_bias_gemma,
            article.sentiment_bielik_explanation, article.sentiment_gemma_explanation,
            article.political_bias_bielik_explanation, article.political_bias_gemma_explanation,
            article.sentiment_gt, article.political_bias_gt
        ])
    
    return response