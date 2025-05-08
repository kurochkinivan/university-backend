from django.db import migrations

def create_test_data(apps, schema_editor):
    Category = apps.get_model('articles', 'Category')
    Tag = apps.get_model('articles', 'Tag')
    Article = apps.get_model('articles', 'Article')
    
    # Создаем категории
    categories = ["Программирование", "Наука", "Искусство", "История", "Технологии"]
    for cat in categories:
        Category.objects.get_or_create(name=cat)
    
    # Создаем теги
    tags = ["Python", "Исследования", "Живопись", "Древний мир", "AI"]
    for tag in tags:
        Tag.objects.get_or_create(name=tag)
    
    # Создаем статьи
    programming_cat = Category.objects.get(name="Программирование")
    science_cat = Category.objects.get(name="Наука")
    art_cat = Category.objects.get(name="Искусство")
    history_cat = Category.objects.get(name="История")
    
    python_tag = Tag.objects.get(name="Python")
    research_tag = Tag.objects.get(name="Исследования")
    painting_tag = Tag.objects.get(name="Живопись")
    ancient_tag = Tag.objects.get(name="Древний мир")
    ai_tag = Tag.objects.get(name="AI")
    
    articles_data = [
        # ... (те же данные, что и в первом варианте)
    ]
    
    for article_data in articles_data:
        article = Article.objects.create(
            name=article_data["name"],
            content=article_data["content"],
            category=article_data["category"],
            excerpt=article_data["excerpt"]
        )
        article.tags.set(article_data["tags"])

class Migration(migrations.Migration):
    dependencies = [
        ('articles', '0006_article_created_at_article_is_active_and_more'),  # Укажите здесь вашу последнюю миграцию
    ]
    
    operations = [
        migrations.RunPython(create_test_data),
    ]