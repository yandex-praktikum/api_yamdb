from reviews.models import Category, Genre, Title  # ,  Comment, Review
# from users.models import User
from .serializers import (CategorySerializer,
                          GenreSerializer, TitleSerializer)
# CommentSerializer, ReviewSerializer)
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet,
                               ):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
#    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
#   permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('year', 'name',) # дописать
    pagination_class = PageNumberPagination


class ReviewViewSet(viewsets.ModelViewSet):

    pass


class CommentViewSet(viewsets.ModelViewSet):

    pass
