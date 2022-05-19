from django_filters import rest_framework as filters 
from reviews.models import Title 

class TitletFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains' )
    genre = filters.CharFilter(field_name="genre__slug", lookup_expr='exact')
    category = filters.CharFilter(field_name="category__slug", lookup_expr='exact')
    year = filters.NumberFilter(field_name='year', lookup_expr='icontains')
    
 
    class Meta:

        model = Title
        fields = ['name', 'category', 'genre', 'year' ]
