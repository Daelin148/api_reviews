from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import (
    Comment, Review, Category, Genre, Title, User, GenreTitle
)


class Command(BaseCommand):

    help = "Загружает данные в БД из csv"

    def load_comments(self):
        with open('comments.csv') as data:
            for row in DictReader(data):
                row['review'] = row.pop('review_id')
                instance = Comment(**row)
                instance.save()

    def load_reviews(self):
        with open('review.csv') as data:
            for row in DictReader(data):
                row['title'] = row.pop('title_id')
                instance = Review(**row)
                instance.save()

    def load_category(self):
        with open('category.csv') as data:
            for row in DictReader(data):
                instance = Category(**row)
                instance.save()

    def load_genre(self):
        with open('genre.csv') as data:
            for row in DictReader(data):
                instance = Genre(**row)
                instance.save()

    def load_title(self):
        with open('titles.csv') as data:
            for row in DictReader(data):
                instance = Title(**row)
                instance.save()

    def load_genre_title(self):
        with open('genre_title.csv') as data:
            for row in DictReader(data):
                row['review'] = row.pop('review_id')
                row['title'] = row.pop('title_id')
                instance = GenreTitle(**row)
                instance.save()

    def load_users(self):
        with open('users.csv') as data:
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
