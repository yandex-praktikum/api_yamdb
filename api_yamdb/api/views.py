from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, permissions
from rest_framework.decorators import action

from api.filters import TitleFilter
from api.mixins import DestroyCreateListMixins, ListCreateDestroyViewSet
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleGetSerializer,
    TitleSerializer,
)
from reviews.filter import TitleFilter
from reviews.models import Category, Comment, Genre, Review, Title
from users.permissions import IsAdminModerOwnerOrReadOnly, IsAdminOrReadOnly


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    """когда будете писать тут функции обработки запросов нужно будет в них
    определять permission_classes=(IsAdminOnly, )"""


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    """когда будете писать тут функции обработки запросов нужно будет в них
    определять permission_classes=(IsAdminOnly, )"""


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


"""когда будете писать тут функции обработки запросов нужно будет в них
    определять permission_classes=(IsAdminOnly, )"""

# Этот метод не работает, ломает ВСЕ тесты, доработать
# def get_serializer_class(self):
#     if self.request.method == 'GET':
#         return TitleGetSerializer
#     return TitleSerializer

# def get_queryset(self):
#     return Title.objects.annotate(
#         rating=Avg('reviews__score'),).order_by('id')


class ReviewViewSet(viewsets.ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = (IsAdminModerOwnerOrReadOnly,)
    """когда будете писать тут функции обработки запросов нужно будет в них
    определять permission_classes=(IsAuthorOrStaff, )"""

    # @action(detail=False,
    #         permission_classes=(IsAuthorOrStaff, ),
    #         methods=['put'])
    def get_queryset(self):

        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    # @action(detail=False,
    #         permission_classes=(IsAuthorOrStaff, ),
    #         methods=['put'])
    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Review, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = (IsAdminModerOwnerOrReadOnly,)

    """когда будете писать тут функции обработки запросов нужно будет в них
    определять permission_classes=(IsAuthorOrStaff, )"""

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
