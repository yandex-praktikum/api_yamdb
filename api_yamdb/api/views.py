from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins

from reviews.models import Category, Genre, Title
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          TitleCreateSerializer)
from .permissions import IsAdminOrReadOnly
from .filters import TitleFilter


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field='slug'


class GenreViewSet(CategoryViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleSerializer
        return TitleCreateSerializer 
