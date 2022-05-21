
from reviews.models import (Category, Genre, Title,
                            Review,
                            TitletFilter)
from users.models import User
from django.shortcuts import get_object_or_404
from .serializers import (CategorySerializer,
                          GenreSerializer, TitleSerializer, TitleGetSerializer,
                          CommentSerializer, ReviewSerializer,
                          UserSerializer, MeSerializer, SignUpSerializer,
                          TokenSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets
from rest_framework import serializers
# from api.validators import check_conformity_title_and_review
from rest_framework.decorators import action, api_view
from .permissions import (ReviewCommentPermission,
                          GenreCategoryPermission,
                          OwnerOrAdmins,
                          IsAdminOrReadOnly,
                          AuthorAndStaffOrReadOnly)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import IntegrityError
from django.core.mail import send_mail
import uuid
from rest_framework_simplejwt.tokens import AccessToken
from django.db.models import Avg


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet,
                               ):
    permission_classes = (GenreCategoryPermission,)
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # filter_backends = (filters.SearchFilter)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitletFilter
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleSerializer
        return TitleGetSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AuthorAndStaffOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        if Review.objects.filter(
                author=self.request.user, title=title).exists():
            raise serializers.ValidationError(
                "Извините, но Вы уже создали один отзыв к данному произведению"
            )
        serializer.save(author=self.request.user, title=title)
        rating_dict = Review.objects.filter(
            title=title).aggregate(Avg("score"))
        new_rating = rating_dict["score__avg"]
        Title.objects.filter(id=title_id).update(rating=new_rating)

    def perform_update(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)
        rating_dict = Review.objects.filter(
            title=title).aggregate(Avg("score"))
        new_rating = rating_dict["score__avg"]
        Title.objects.filter(id=title_id).update(rating=new_rating)


class CommentViewSet(viewsets.ModelViewSet):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentPermission, AuthorAndStaffOrReadOnly)

    def get_queryset(self):
        # Получаем id котика из эндпоинта
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        # И отбираем только нужные комментарии
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (OwnerOrAdmins, )
    filter_backends = (filters.SearchFilter, )
    filterset_fields = ('username')
    search_fields = ('username', )
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated, )
    )
    def get_patch_me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup_post(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    try:
        (user, result) = User.objects.get_or_create(
            username=username,
            email=email
        )
    except IntegrityError:
        return Response(
            'Такой логин или email уже существуют',
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = str(uuid.uuid4())
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        'Код подверждения', confirmation_code,
        ['admin@email.com'], (email, ), fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def token_post(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user_base = get_object_or_404(User, username=username)
    if confirmation_code == user_base.confirmation_code:
        token = str(AccessToken.for_user(user_base))
        return Response({'token': token}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
