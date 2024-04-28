from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from reviews.models import Category, Genre, Title

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    http_method_names = ['get', 'post',
                         'patch', 'delete']

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year',
                        'category__slug', 'genre__slug'
                        )

    def get_queryset(self):
        queryset = Title.objects.all(
        ).select_related('category').prefetch_related('genre')
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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)
