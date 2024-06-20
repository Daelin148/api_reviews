from csv import DictReader

from core.models import User
from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title

DATA_DIR = settings.STATICFILES_DIRS[0] / 'data'


class Command(BaseCommand):

    help = "Загружает данные в БД из csv"

    def load_comments(self):
        with open(DATA_DIR / 'comments.csv', encoding='utf-8') as data:
            for row in DictReader(data):
                row['author_id'] = row.pop('author')
                instance = Comment(**row)
                instance.save()

    def load_reviews(self):
        with open(DATA_DIR / 'review.csv', encoding='utf-8') as data:
            for row in DictReader(data):
                row['author_id'] = row.pop('author')
                instance = Review(**row)
                instance.save()

    def load_category(self):
        with open(DATA_DIR / 'category.csv', encoding='utf-8') as data:
            for row in DictReader(data):
                instance = Category(**row)
                instance.save()

    def load_genre(self):
        with open(DATA_DIR / 'genre.csv', encoding='utf-8') as data:
            for row in DictReader(data):
                instance = Genre(**row)
                instance.save()

    def load_title(self):
        with open(DATA_DIR / 'titles.csv', encoding='utf-8') as data:
            for row in DictReader(data):
                row['category_id'] = row.pop('category')
                instance = Title(**row)
                instance.save()

    def load_genre_title(self):
        with open(DATA_DIR / 'genre_title.csv', encoding='utf-8') as data:
            for row in DictReader(data):
                title = Title.objects.get(pk=row['title_id'])
                genre = Genre.objects.get(pk=row['genre_id'])
                title.genre.add(genre)

    def load_users(self):
        with open(DATA_DIR / 'users.csv', encoding='utf-8') as data:
            for row in DictReader(data):
                instance = User(**row)
                instance.save()

    def handle(self, *args, **options):
        self.load_users()
        self.load_genre()
        self.load_category()
        self.load_title()
        self.load_genre_title()
        self.load_reviews()
        self.load_comments()
