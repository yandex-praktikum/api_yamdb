from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleModelFilter
from .models import Review, Title, User, Category, Genre
from .permissions import IsAdminOrReadOnly, IsAdminModeratorOrAuthor
from .serializers import (
    EmailSerializer, TitleReadSerializer, TitleWriteSerializer,
    TokenObtainPairSerializer, UserSerializer, CategorySerializer,
    GenreSerializer, ReviewSerializer, CommentSerializer
)


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
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        self.kwargs['username'] = request.user.username
        if request.method == 'GET':
            return self.retrieve(request)
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save(role=request.user.role)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_new_user(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if User.objects.filter(email=serializer.validated_data['email']).exists():
        try:
            send_confirmation_code(serializer.validated_data['email'])
        except RuntimeError:
            return Response(
                'Ошибка отправки почты',
                status=status.HTTP_502_BAD_GATEWAY
            )
        return Response(
            'Confirmation code  отправлен на ваш email',
            status=status.HTTP_200_OK
        )
    User.objects.create_user(
        username=serializer.instance['email'],
        email=serializer.instance['email']
    )
    try:
        send_confirmation_code(serializer.instance['email'])
    except RuntimeError:
        Response(
            'Ошибка отправки почты',
            status=status.HTTP_502_BAD_GATEWAY
        )
    return Response(
        'Пользователь успешно создан и отправлен email с confirmation code',
        status=status.HTTP_201_CREATED
    )


def send_confirmation_code(email):
    user = get_object_or_404(User, email=email)
    confirmation_code = default_token_generator.make_token(user)
    try:
        send_mail(
            'Ваш код подтверждения YaMDb',
            f'Код подтверждения:{confirmation_code}',
            settings.EMAIL_HOST_USER + settings.EMAIL_HOST_DOMEN,
            (email,),
        )
    except BaseException:
        raise RuntimeError


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
    filter_class = TitleModelFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminModeratorOrAuthor,
    )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminModeratorOrAuthor,
    )

    def _get_review_id(self):
        return self.kwargs.get('review_id')

    def _get_title_id(self):
        return self.kwargs.get('title_id')

    def get_queryset(self):
        review = get_object_or_404(
            Review, pk=self._get_review_id(), title__id=self._get_title_id()
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, pk=self._get_review_id(), title__id=self._get_title_id()
        )
        serializer.save(author=self.request.user, review=review)


@api_view(['POST'], )
@permission_classes([AllowAny])
def token_obtain_pair_view(request):
    serializer = TokenObtainPairSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, email=serializer.validated_data['email'])
    token = AccessToken.for_user(user)
    data = {'token': str(token)}
    return Response(data)
