import os
import random
from datetime import date
from django.core.management.base import BaseCommand
from django.core.files import File
from catalog.models import Author, Genre, Library, Book
from django.conf import settings


class Command(BaseCommand):
    help = 'Seed the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing old data...')
        Book.objects.all().delete()
        Author.objects.all().delete()
        Genre.objects.all().delete()
        Library.objects.all().delete()

        self.stdout.write('Creating libraries...')
        libraries = [
            Library.objects.create(name='Central Library', address='123 Main St'),
            Library.objects.create(name='East Side Library', address='456 East Ave')
        ]

        self.stdout.write('Creating genres...')
        genre_names = ['Fiction', 'Science', 'Fantasy', 'History', 'Romance']
        genres = [Genre.objects.create(name=name) for name in genre_names]

        self.stdout.write('Creating authors...')
        authors = [
            Author.objects.create(name='John Smith', birth_date='1975-06-15'),
            Author.objects.create(name='Jane Doe', birth_date='1980-09-10'),
            Author.objects.create(name='Albert Einstein', birth_date='1879-03-14'),
        ]

        self.stdout.write('Creating books with images...')
        images_dir = os.path.join(settings.BASE_DIR, 'catalog', 'seed_images')
        image_files = sorted([f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png'))])

        for i in range(10):
            image_path = os.path.join(images_dir, image_files[i % len(image_files)])
            with open(image_path, 'rb') as img_file:
                book = Book.objects.create(
                    title=f'Book {i + 1}',
                    publication_date=date(2000 + i, 1, 1),
                    isbn=f'1234567890{i:03}',
                    price=round(random.uniform(10.0, 100.0), 2),
                    rating=random.uniform(0, 5),
                    image=File(img_file, name=image_files[i % len(image_files)]),
                    library=random.choice(libraries)
                )
                book.authors.set(random.sample(authors, k=random.randint(1, 2)))
                book.genres.set(random.sample(genres, k=random.randint(1, 3)))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully.'))
