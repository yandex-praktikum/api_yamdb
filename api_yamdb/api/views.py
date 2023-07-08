from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitlesFilter
from .permissions import IsAdmin, IsAdminModeratorOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import (
    CategoriesSerializer, CommentSerializer, GenresSerializer,
    ReviewSerializer, TitlesGetSerializer,
    TitlesPostSerializer, UserEditSerializer, UserSerializer
)


class CategoryGenreViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Mixin for Category and Genre models."""
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['post', 'get', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def user_me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments_reviews.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return (permissions.IsAuthenticated(),)
        return (IsAdminModeratorOwnerOrReadOnly(),)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews_title.all().order_by('id')

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user,
                        title=title)


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesGetSerializer
        return TitlesPostSerializer
