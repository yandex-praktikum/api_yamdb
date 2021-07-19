from smtplib import SMTPException

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import EMAIL_HOST_USER, EMAIL_HOST_DOMEN
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

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(IsMeAction,)
    )
    def me(self, request):
        self.kwargs['username'] = request.user.username
        if request.method == 'GET':
            return self.retrieve(request)
        return self.partial_update(request)


def get_confirmation_code(user):
    return default_token_generator.make_token(user)


@api_view(['POST'], )
@permission_classes([AllowAny])
def CreateNewUser(request):
    serializer = EmailSerializer(data=request.data)
    user_max_pk = User.objects.latest('pk')
    max_pk = user_max_pk.pk
    username = ('user' + str(max_pk + 1))
    if serializer.is_valid():
        serializer.save(
            username=username
        )
        send_confirmation_code(username, [serializer.data['email']])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if serializer.errors['email'][0] == (
            'user with this email address already exists.'
    ):
        send_confirmation_code(username, [serializer.data['email']])
        return Response(
            'Confirmation code повторно отправлен на ваш email',
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_confirmation_code(username, email):
    try:
        user = get_object_or_404(User, username=username)
        confirmation_code = get_confirmation_code(user)
        send_mail(
            'Your confirmation code YaMDb',
            f'Confirmation code:{confirmation_code}',
            EMAIL_HOST_USER + EMAIL_HOST_DOMEN,
            email,
        )
    except SMTPException as e:
        print('There was an error sending an email: ', e)


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
        if self.action in ('retrieve', 'list'):
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

    def _get_review_id(self):
        return self.kwargs.get('review_id')

    def get_title_id(self):
        return self.kwargs.get('title_id')

    def get_queryset(self):
        review = get_object_or_404(
            Review, pk=self._get_review_id(), title__id=self.get_title_id()
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, pk=self._get_review_id(), title__id=self.get_title_id()
        )
        serializer.save(author=self.request.user, review=review)


def get_token(user):
    return AccessToken.for_user(user)


@api_view(['POST'], )
@permission_classes([AllowAny])
def TokenObtainPairView(request):
    serializer = TokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, email=serializer.initial_data['email'])
        token = get_token(user)
        data = {'token': str(token)}
        return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
