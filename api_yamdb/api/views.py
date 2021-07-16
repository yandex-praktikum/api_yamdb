
from requests import Response
from collections import OrderedDict
from django_filters.rest_framework import DjangoFilterBackend
from random import randint
from django.shortcuts import get_object_or_404 
from django.core.mail import send_mail


from rest_framework import viewsets, mixins, filters, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.response import Response 

from .models import User, Categories, Genres, Titles, Review
from .permissions import IsAdminOrReadOnly
from .serializers import (
    UserSerializer, EmailSerializer, CategoriesSerializer, GenresSerializer,
    TitlesPostSerializer, TitlesGetSerializer, ReviewSerializer, TokenObtainPairSerializer,
    CommentSerializer
)


class CreateViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    pass


class CreateListViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
            [serializer.data['email'], ],
        )


class CategoriesViewSet(CreateListViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)

    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(CreateListViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return TitlesGetSerializer 
        return TitlesPostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

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

# token_obtain_pair = TokenObtainPairView.as_view()
