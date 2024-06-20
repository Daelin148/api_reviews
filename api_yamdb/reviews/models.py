from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import AuthorPubDateText, NameBaseModel, NameSlugBaseModel
from core.validators import validate_year


class Category(NameSlugBaseModel):
    """Модель категорий."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Genre(NameSlugBaseModel):
    """Модель жанров."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


class Title(NameBaseModel):
    """Модель произведений."""

    year = models.SmallIntegerField(verbose_name='Год выпуска',
                                    validators=(validate_year,))
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')
    genre = models.ManyToManyField(Genre, verbose_name='Жанры')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='titles', null=True,
                                 blank=True, verbose_name='Категория')

    class Meta:
        ordering = ('year', )
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(AuthorPubDateText):
    """Модель отзывов."""

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
        ordering = ('-score',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]


class Comment(AuthorPubDateText):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ('-pub_date',)
