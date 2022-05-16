from reviews.models import Category, Genre, Title, Comment, Review
from users.models import User
from django.shortcuts import get_object_or_404
from .serializers import (CategorySerializer,
                          GenreSerializer, TitleSerializer,
                          CommentSerializer, ReviewSerializer)

from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets, serializers, filters
from .permissions import ReviewCommentPermission, GenreCategoryPermission
from .validations import check_conformity_title_and_review




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
    permission_classes = (GenreCategoryPermission,) 
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (GenreCategoryPermission,) 
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('year', 'name',) # дописать
    pagination_class = PageNumberPagination
#дописать

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        if Review.objects.filter(author=self.request.user,
                                 title_id=title).exists():
            raise serializers.ValidationError(
                "Извините, но Вы уже создали один отзыв к данному произведению"
            )
        serializer.save(author=self.request.user, title_id=title)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentPermission, )

    def get_queryset(self):
        check_conformity_title_and_review(self)
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        check_conformity_title_and_review(self)
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review_id=review)