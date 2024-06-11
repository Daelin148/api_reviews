import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug')
    genre = django_filters.CharFilter(field_name='genres__slug')
    name = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.NumberFilter()

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
