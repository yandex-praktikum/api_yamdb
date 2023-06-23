from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action

from api.mixins import DestroyCreateListMixins
from api.serializers import (CategoriesSerializer, CommentSerializer,
                             GenresSerializer, ReviewSerializer,
                             TitlesGetSerializer, TitlesSerializer)
from reviews.filter import TitleFilter
from reviews.models import Categories, Comments, Genres, Reviews, Titles
from users.permissions import GuestReadOnly, IsAdminOnly, IsAuthorOrStaff


class CategoryViewSet(DestroyCreateListMixins):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (GuestReadOnly, )

    """когда будете писать тут функции обработки запросов нужно будет в них
    определять permission_classes=(IsAdminOnly, )"""


class GenreViewSet(DestroyCreateListMixins):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (GuestReadOnly, )
    """когда будете писать тут функции обработки запросов нужно будет в них
    определять permission_classes=(IsAdminOnly, )"""


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (GuestReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
"""когда будете писать тут функции обработки запросов нужно будет в них
    определять permission_classes=(IsAdminOnly, )"""

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesGetSerializer
        return TitlesSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (GuestReadOnly, )
    """когда будете писать тут функции обработки запросов нужно будет в них
    определять permission_classes=(IsAuthorOrStaff, )"""

    # @action(detail=False,
    #         permission_classes=(IsAuthorOrStaff, ),
    #         methods=['put'])
    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(
            Titles,
            pk=title_id)
        return title.reviews.all()

    # @action(detail=False,
    #         permission_classes=(IsAuthorOrStaff, ),
    #         methods=['put'])
    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(
            Reviews,
            pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (GuestReadOnly, )

    """когда будете писать тут функции обработки запросов нужно будет в них
    определять permission_classes=(IsAuthorOrStaff, )"""

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Reviews,
            pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Reviews,
            pk=review_id)
        serializer.save(author=self.request.user, review=review)
