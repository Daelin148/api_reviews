from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import (
    Category, Comment, Genre, GenreTitle, Review, Title
)
from core.models import User


class Command(BaseCommand):

    help = "Загружает данные в БД из csv"

    def load_comments(self):
        with open('data/comments.csv') as data:
            for row in DictReader(data):
                row['review'] = row.pop('review_id')
                instance = Comment(**row)
                instance.save()

    def load_reviews(self):
        with open('data/review.csv') as data:
            for row in DictReader(data):
                row['title'] = row.pop('title_id')
                instance = Review(**row)
                instance.save()

    def load_category(self):
        with open('data/category.csv') as data:
            for row in DictReader(data):
                instance = Category(**row)
                instance.save()

    def load_genre(self):
        with open('data/genre.csv') as data:
            for row in DictReader(data):
                instance = Genre(**row)
                instance.save()

    def load_title(self):
        with open('data/titles.csv') as data:
            for row in DictReader(data):
                instance = Title(**row)
                instance.save()

    def load_genre_title(self):
        with open('data/genre_title.csv') as data:
            for row in DictReader(data):
                row['review'] = row.pop('review_id')
                row['title'] = row.pop('title_id')
                instance = GenreTitle(**row)
                instance.save()

    def load_users(self):
        with open('data.users.csv', encoding='utf-8') as data:
            for row in DictReader(data):
                instance = User(**row)
                instance.save()

    def handle(self, *args, **options):
        self.load_users()
        self.load_genre()
        self.load_category()
        self.load_title()
        self.load_reviews()
        self.load_comments()
