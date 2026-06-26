from django.db import migrations


def create_default_dataset(apps, schema_editor):
    """Assign all existing NewsArticles (without a dataset) to a default Dataset."""
    Dataset = apps.get_model('annotator', 'Dataset')
    NewsArticle = apps.get_model('annotator', 'NewsArticle')

    orphan_articles = NewsArticle.objects.filter(dataset__isnull=True)
    if orphan_articles.exists():
        dataset = Dataset.objects.create(
            name='Zestaw domyślny',
            csv_filename='(istniejące dane)',
        )
        orphan_articles.update(dataset=dataset)


def reverse_default_dataset(apps, schema_editor):
    """Reverse: unset dataset on all articles and delete the default dataset."""
    Dataset = apps.get_model('annotator', 'Dataset')
    NewsArticle = apps.get_model('annotator', 'NewsArticle')

    try:
        dataset = Dataset.objects.get(name='Zestaw domyślny')
        NewsArticle.objects.filter(dataset=dataset).update(dataset=None)
        dataset.delete()
    except Dataset.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('annotator', '0003_add_dataset_model'),
    ]

    operations = [
        migrations.RunPython(create_default_dataset, reverse_default_dataset),
    ]
