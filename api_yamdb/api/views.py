from random import randint

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework_simplejwt.views import TokenViewBase

from .filters import ModelFilter
from .models import Category, Genre, Review, Title, User
from .permissions import (
    IsAdminModeratorOrAuthor,
    IsAdminOrReadOnly, IsMeAction
)
from .serializers import (
  CategorySerializer, CommentSerializer,
  EmailSerializer, GenreSerializer, ReviewSerializer,
  TitleReadSerializer, TitleWriteSerializer,
  TokenObtainPairSerializer, UserSerializer
)



class CreateViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    pass


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(detail=False, methods=['GET', 'PATCH'], permission_classes=(IsMeAction,))
    def me(self, request):
        self.kwargs['username'] = request.user.username
        if request.method == 'GET':
            return self.retrieve(request)
        elif request.method == 'PATCH':
            return self.partial_update(request)
        else:
            raise Exception('Not implemented')


class EmailViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = EmailSerializer

    def perform_create(self, serializer):
        confirmation_code = randint(100000, 999999)
        serializer.save(confirmation_code=confirmation_code)
        send_mail(
            'Your confirmation code YaMDb',
            f'Confirmation code:{confirmation_code}',
            'django.test1.mail@gmail.com',
            [serializer.data['email']],
        )


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)

    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filter_class = ModelFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminModeratorOrAuthor,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminModeratorOrAuthor,)

    def get_review_id(self):
        return self.kwargs.get('review_id')

    def get_title_id(self):
        return self.kwargs.get('title_id')

    def get_queryset(self):
        review = get_object_or_404(
            Review, pk=self.get_review_id(), title__id=self.get_title_id()
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, pk=self.get_review_id(), title__id=self.get_title_id()
        )
        serializer.save(author=self.request.user, review=review)


class TokenObtainPairView(TokenViewBase):
    serializer_class = TokenObtainPairSerializer
