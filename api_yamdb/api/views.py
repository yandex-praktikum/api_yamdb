from rest_framework import viewsets
from reviews.models import Category, Genre, Title
from .mixins import ListCreateDestroyViewSet
from .serializers import (
    CategoriesSerializer, GenresSerializer,
    TitlesPostSerializer, ReviewSerializer,
    CommentSerializer)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesPostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
