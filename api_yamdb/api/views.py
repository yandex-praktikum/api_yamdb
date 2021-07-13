from requests import Response
from rest_framework import viewsets, status, mixins, permissions, filters
from .permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
    )

from .models import User, Categories, Genres, Titles
from .serializers import UserSerializer, EmailSerializer, CategoriesSerializer, GenresSerializer, TitlesSerializer

class CreateViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    pass

class CreateListViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EmailViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = EmailSerializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriesViewSet(CreateListViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

class GenresViewSet(CreateListViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

class TitlesViewSet(CreateListViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer       