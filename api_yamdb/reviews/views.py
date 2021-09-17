from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets

from reviews.models import Category, Genre, Review, Title
from reviews.serializers import (CategorySerializer, CommentSerializer,
                                 GenreSerializer, ReviewSerializer,
                                 TitleSerializer, TitleSerializerCreate)
from .permissions import (IsAdminOrReadOnlyPermissions, IsOwnerOrReadOnlyPermissions,
                               IsStaffOrReadOnlyPermissions)

from .filters import TitleFilter


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class GenresViewSet(ListCreateDestroyViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnlyPermissions
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class CategoriesViewSet(ListCreateDestroyViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsStaffOrReadOnlyPermissions,
        IsAdminOrReadOnlyPermissions
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsStaffOrReadOnlyPermissions,
        IsAdminOrReadOnlyPermissions
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('id')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return TitleSerializerCreate


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnlyPermissions
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnlyPermissions
    ]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            title__id=self.kwargs['title_id'],
            id=self.kwargs['review_id'],
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)
