from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from reviews.models import (Categories,
                            Genres,
                            Titles,
                            Reviews,
                            Comments)
from reviews.filter import TitleFilter
from api.mixins import DestroyCreateListMixins
from api.serializers import (CategoriesSerializer,
                             GenresSerializer,
                             TitleGenreSerializer,
                             ReviewSerializer,
                             TitlesSerializer,
                             CommentSerializer)
from users.permissions import (IsAdminOrReadOnly)


class CategoryViewSet(DestroyCreateListMixins):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly]


class GenreViewSet(DestroyCreateListMixins):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsAdminOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGenreSerializer
        return TitlesSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(
            Titles,
            pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(
            Reviews,
            pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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
