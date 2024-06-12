from core.models import AuthorPubDateText, NameBaseModel, NameSlugBaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(NameSlugBaseModel):
    """Модель категорий."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugBaseModel):
    """Модель жанров."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(NameBaseModel):
    """Модель произведений."""

    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')
    genres = models.ManyToManyField(Genre, through='GenreTitle',
                                    verbose_name='Жанры')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='titles', null=True,
                                 verbose_name='Категория')

    class Meta:
        ordering = ('year', )
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    """Промежуточная модель для связи жанров и произведений."""

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title.name} - {self.genre.name}'


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


class Comment(AuthorPubDateText):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
