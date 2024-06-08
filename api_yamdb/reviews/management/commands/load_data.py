from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Comment, Review, Category, Genre, Title, User


class Command(BaseCommand):

    help = "Загружает данные в БД из csv"

    def load_comments(self):
        with open('comments.csv') as data:
            for row in DictReader(data):
                instance = Comment(
                    id=row['id'], text=row['text'],
                    author=row['author'], pub_date=row['pub_date'],
                    review=row['review_id']
                )
                instance.save()

    def load_reviews(self):
        with open('review.csv') as data:
            for row in DictReader(data):
                instance = Review(
                    id=row['id'], text=row['text'],
                    author=row['author'], pub_date=row['pub_date'],
                    title=row['title_id'], score=row['score'],
                )
                instance.save()

    def load_category(self):
        with open('category.csv') as data:
            for row in DictReader(data):
                instance = Category(
                    id=row['id'], name=row['name'],
                    slug=row['slug']
                )
                instance.save()

    def load_genre(self):
        with open('genre.csv') as data:
            for row in DictReader(data):
                instance = Genre(
                    id=row['id'], name=row['name'],
                    slug=row['slug']
                )
                instance.save()

    def load_title(self):
        with open('titles.csv') as data:
            for row in DictReader(data):
                instance = Title(
                    id=row['id'], name=row['name'],
                    year=row['year'], category=row['category']
                )
                instance.save()

    def load_genre_title(self):
        with open('genre_title.csv') as data:
            for row in DictReader(data):
                instance = Category(
                    id=row['id'], title_id=row['title_id'],
                    genre_id=row['genre_id']
                )
                instance.save()

    def load_users(self):
        with open('users.csv') as data:
            for row in DictReader(data):
                instance = User(
                    id=row['id'], username=row['username'],
                    email=row['email'], role=row['role'],
                    bio=row['bio'], first_name=row['first_name'],
                    last_name=row['last_name']
                )
                instance.save()

    def handle(self, *args, **options):
        self.load_users()
        self.load_genre()
        self.load_category()
        self.load_title()
        self.load_reviews()
        self.load_comments()
