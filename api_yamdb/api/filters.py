import django_filters

from .models import Titles


class ModelFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug',
                                      lookup_expr='icontains')

    category = django_filters.CharFilter(field_name='category__slug',
                                         lookup_expr='icontains')

    name = django_filters.CharFilter(field_name='name',
                                     lookup_expr='icontains')

    class Meta:
        model = Titles
        fields = ('genre', 'category', 'year', 'name')
