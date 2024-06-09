from core.models import AuthorPubDateText
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Title(models.Model):
    pass


class Review(AuthorPubDateText):
    """Модель отзывов"""

    score = models.IntegerField(
        'Рейтинг',
        validators=(MinValueValidator(1), MaxValueValidator(10))
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        verbose_name='Заголовок',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'


class Comment(AuthorPubDateText):
    """Модель комментариев"""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
