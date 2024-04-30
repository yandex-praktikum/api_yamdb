from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from reviews.models import Category, Genre, Title, Review

from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleSerializer, ReviewSerializer,
    CommentSerializers
    )
from django.shortcuts import get_object_or_404

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    http_method_names = ['get', 'post',
                         'patch', 'delete']

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year',
                        'category__slug', 'genre__slug'
                        )

    def get_queryset(self):
        queryset = Title.objects.all(
        ).select_related('category').prefetch_related('genre')
        category_slug = self.request.query_params.get('category')
        genre_slug = self.request.query_params.get('genre')
        if (category_slug is not None) and (genre_slug is not None):
            queryset = queryset.filter(
                category__slug=category_slug, genre__slug=genre_slug)
        if category_slug is not None:
            queryset = queryset.filter(category__slug=category_slug)
        if genre_slug is not None:
            queryset = queryset.filter(genre__slug=genre_slug)
        return queryset


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (пермишн автор, модератор, админ)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializers
    # permission_classes = (пермишн автор, модератор, админ)

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