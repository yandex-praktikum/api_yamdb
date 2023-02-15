from rest_framework import viewsets, pagination
from reviews.models import Category, Genre, Title
from .permissions import IsAdminOrReadOnly
from .serializers import (
    GenreSerializer,
    GenreSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleGetSerializer
    serializer_class = TitlePostSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TitlePostSerializer
        return TitleGetSerializer
