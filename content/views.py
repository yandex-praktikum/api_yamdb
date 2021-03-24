from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleReadSerializer, TitleWriteSerializer
)

from .filters import TitleFilter
from .models import Category, Genre, Title


class CreateDestroyListRetrieveViewSet(mixins.CreateModelMixin,
                                       mixins.ListModelMixin,
                                       mixins.DestroyModelMixin,
                                       viewsets.GenericViewSet):
    pass


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class GenreViewSet(CreateDestroyListRetrieveViewSet):
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CreateDestroyListRetrieveViewSet):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
