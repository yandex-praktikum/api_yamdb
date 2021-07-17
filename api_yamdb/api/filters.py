from django_filters import CharFilter, FilterSet

from .models import User


class UserFilter(FilterSet):
    search = CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ('search',)
