from rest_framework import status, viewsets
from rest_framework.response import Response
from users.permissions import IsAdmin

from titles.models import Category, Genre, Title

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_class = IsAdmin

    def update(self, request, *args, **kwargs):
        return Response({"detail": "PUT method is not allowed."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    """Вьюсет для произведений."""


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Получить список всех категорий. Права доступа: Доступно без токена
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # filter_backends = (добавить,)


