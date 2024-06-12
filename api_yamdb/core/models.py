from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class NameBaseModel(models.Model):
    """Абстрактная модель с полем name и строковым представлением."""

    name = models.CharField(max_length=256, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class NameSlugBaseModel(NameBaseModel):
    """Абстрактная модель с полем slug."""

    slug = models.SlugField(unique=True, max_length=50, verbose_name='Слаг')

    class Meta:
        abstract = True


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
