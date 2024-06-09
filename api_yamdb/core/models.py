from django.db import models
from reviews.models import User


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