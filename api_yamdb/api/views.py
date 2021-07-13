from random import randint

from django.core.mail import send_mail
from rest_framework import viewsets, mixins, filters
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)

from .models import User, Categories, Genres, Titles
from .permissions import IsAdminOrReadOnly
from .serializers import UserSerializer, EmailSerializer, CategoriesSerializer, GenresSerializer, TitlesSerializer, \
    ReviewSerializer


class CreateViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    pass


class CreateListViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
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
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
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


class TitlesViewSet(CreateListViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


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
