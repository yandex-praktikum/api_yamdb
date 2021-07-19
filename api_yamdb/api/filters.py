from django_filters import CharFilter, FilterSet

from .models import Titles


class TitlesFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Titles
        fields = ('name', 'year', 'genre', 'category')
