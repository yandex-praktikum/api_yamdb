from django.db.models import Avg
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets

from api.filters import TitleFilter
from api.permissions import (AdminOrReadOnlyAccess,
                             AuthorOrModeratorOrAdminAccess)
from api.serializers import (CategorySerializer, CommentSerializers,
                             GenreSerializer, ReviewSerializer,
                             TitleCreateUpdateSerializer, TitleReadSerializer)
from reviews.models import Category, Genre, Review, Title


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleReadSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    ordering_fields = ('name', 'year', 'rating')
    http_method_names = ['get', 'post',
                         'patch', 'delete']
    permission_classes = (AdminOrReadOnlyAccess,)

    def get_queryset(self):
        queryset = Title.objects.annotate(rating=Round(Avg('reviews__score')))
        return queryset

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleReadSerializer
        return TitleCreateUpdateSerializer


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', 'slug',)
    ordering_fields = ('name')
    permission_classes = (AdminOrReadOnlyAccess,)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrModeratorOrAdminAccess,)
    http_method_names = ['get', 'post',
                         'patch', 'delete']
    lookup_field = 'id'

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        new_queryset = Review.objects.filter(title_id=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title.objects, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializers
    permission_classes = (AuthorOrModeratorOrAdminAccess,)
    http_method_names = ['get', 'post',
                         'patch', 'delete']
    lookup_field = 'id'

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)
