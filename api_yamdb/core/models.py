from reviews.models import User
from django.db import models


class NameSlugBaseModel(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=50, verbose_name='Слаг')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class AuthorPubDateText(models.Model):
    """Абстрактная модель, добавляющая
    общие поля для моделей отзывов и комментариев."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField('Содержание')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
