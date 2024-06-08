from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Title(models.Model):
    pass

class Review(models.Model):
    """Модель отзывов"""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор отзыва'
    )
    text = models.TextField('Содержание отзыва')
    score = models.IntegerField(
        'Рейтинг',
        validators=(MinValueValidator(1), MaxValueValidator(10))
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        verbose_name='Заголовок',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'


class Comment(models.Model):
    """Модель комментариев"""

    text = models.TextField('Содержание комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
