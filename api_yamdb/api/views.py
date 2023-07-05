from rest_framework import viewsets
from reviews.models import Category, Genre, Title, User, Review, Comment
from .mixins import ListCreateDestroyViewSet
from .serializers import (
    CategoriesSerializer, GenresSerializer,
    TitlesPostSerializer, ReviewSerializer,
    CommentSerializer)
from .permissions import (
    IsAdminOrSuperUser, IsAdminOrReadOnly, IsAuthorOrIsStaff
)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly]

class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsAdminOrReadOnly]

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesPostSerializer
    permission_classes = [IsAdminOrReadOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrIsStaff]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrIsStaff]
