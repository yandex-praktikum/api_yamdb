# from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets  # , permissions
# from rest_framework.decorators import action

from api.filters import TitleFilter
from api.mixins import ListCreateDestroyViewSet  # DestroyCreateListMixins,
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleGetSerializer,
    TitleSerializer,
)
#from api.filters import TitleFilter
from reviews.models import Category, Genre, Review, Title  # Comment,
from users.permissions import IsAdminOnly, IsAdminModerOwnerOrReadOnly, IsAdminOrReadOnly
# GuestReadOnly, IsAuthorOrStaff,


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitleSerializer

# def get_queryset(self):
#     return Title.objects.annotate(
#         rating=Avg('reviews__score'),).order_by('id')


class ReviewViewSet(viewsets.ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModerOwnerOrReadOnly,)

    # @action(detail=False,
    #         permission_classes=(IsAuthorOrStaff, ),
    #         methods=['put'])
    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    # @action(detail=False,
    #         permission_classes=(IsAuthorOrStaff, ),
    #         methods=['put'])
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModerOwnerOrReadOnly,)


    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review=get_object_or_404(
                            Review,
                            pk=self.kwargs.get('review_id'),),)
