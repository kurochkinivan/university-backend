from django.core.management.base import BaseCommand
from faker import Faker
from articles.models import Article, Category, Tag  
import random

# python manage.py seed_articles 10 --max-tags 5
class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми статьями, категориями и тегами'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Количество статей для создания')
        parser.add_argument('--max-tags', type=int, default=3, help='Максимальное количество тегов на статью')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        max_tags = kwargs.get('max_tags', 3)
        fake = Faker()

        # Создаем несколько категорий, если их мало
        if Category.objects.count() < 5:
            for _ in range(5):
                Category.objects.create(name=fake.word())

        # Создаем несколько тегов, если их мало
        if Tag.objects.count() < 10:
            for _ in range(10):
                Tag.objects.create(name=fake.word())

        categories = list(Category.objects.all())
        tags = list(Tag.objects.all())

        for _ in range(total):
            category = random.choice(categories)

            article = Article.objects.create(
                name=fake.sentence(nb_words=6),
                content=fake.text(max_nb_chars=2000),
                featured_image="default.jpg",
                category=category,
            )

            # Добавляем рандомные теги
            selected_tags = random.sample(tags, k=random.randint(1, min(max_tags, len(tags))))
            article.tags.set(selected_tags)

        self.stdout.write(self.style.SUCCESS(f'Успешно создано {total} статей с категориями и тегами'))