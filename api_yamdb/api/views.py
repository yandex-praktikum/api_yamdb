from rest_framework import mixins, viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters import ModelChoiceFilter, NumberFilter, CharFilter

from reviews.models import Category, Genre, Title

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .permissions import AdminOrReadOnly


# class RelatedFilterSet(FilterSet):
#     category = CharFilter(field_name='category__slug')
#     genre = CharFilter(field_name='genre__slug')

#     # def filter_category(self, queryset, name, value):
#     #     return queryset.filter(category__slug=value)

#     class Meta:
#         model = Title
#         fields = ('name', 'year', 'category', 'genre')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    http_method_names = ['get', 'post',
                         'patch', 'delete']
    # permission_class = (AdminOrReadOnly)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year',
                        'category__slug', 'genre__slug'
                        )
    # filter_class = RelatedFilterSet
    # filter_fields = ('category', 'genre')

    def get_queryset(self):
        queryset = Title.objects.all().select_related('category').prefetch_related('genre')
        category_slug = self.request.query_params.get('category')
        genre_slug = self.request.query_params.get('genre')
        if (category_slug is not None) and (genre_slug is not None):
            queryset = queryset.filter(
                category__slug=category_slug, genre__slug=genre_slug)
        if category_slug is not None:
            queryset = queryset.filter(category__slug=category_slug)
        if genre_slug is not None:
            queryset = queryset.filter(genre__slug=genre_slug)
        return queryset


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    # permission_class = (AdminOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    # permission_class = (AdminOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)
