from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        USER = 'user'
        ADMIN = 'admin'
        MODERATOR = 'moderator'

    username = models.CharField(
        'Имя пользователя',
        max_length=settings.LIMIT_USERNAME,
        unique=True,
        blank=False,
        null=False,
        validators=(validate_username,)
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=settings.LIMIT_EMAIL,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.LIMIT_FIRST_NAME,
        blank=True,
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=settings.LIMIT_LAST_NAME,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=settings.LIMIT_ROLE,
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (self.role == self.RoleChoices.ADMIN or
                self.is_superuser or
                self.is_staff)

    @property
    def is_moderator(self):
        return self.role == self.RoleChoices.MODERATOR


class NameBaseModel(models.Model):
    """Абстрактная модель с полем name и строковым представлением."""

    name = models.CharField(max_length=settings.LIMIT_NAME, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class NameSlugBaseModel(NameBaseModel):
    """Абстрактная модель с полем slug."""

    slug = models.SlugField(unique=True, max_length=settings.LIMIT_SLUG, verbose_name='Слаг')

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
