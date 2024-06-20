import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            'Недопустимое имя пользователя!'
        )
    if not bool(re.match(r'^[\w.@+-]+$', value)):
        raise ValidationError(
            'Некорректные символы в username'
        )
    return value


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError('Год выпуска не может быть больше текущего года')
    if value <= 0:
        raise ValidationError('Год выпуска должен быть положительным числом.')
