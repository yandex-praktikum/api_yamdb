from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User, Genre, Category, Title
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import (RegisterSerializer, TokenSerializer,
                          UserSerializer, GenreSerializer,
                          CategorySerializer, TitleReadSerializer,
                          TitleWriteSerializer)
from .sendtoken import make_token


class RegistrationView(CreateAPIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if User.objects.filter(username=request.data.get('username'),
                               email=request.data.get('email')).exists():
            user = User.objects.get(username=request.data.get('username'))
            return Response(
                {'Новый токен': str(RefreshToken.for_user(user).access_token)},
                status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        make_token(User.objects.get(
            username=serializer.validated_data['username']))
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(CreateAPIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username'])
        if (serializer.validated_data['confirmation_code']
                != user.confirmation_code):
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST
                            )
        return Response(
            {'token': str(RefreshToken.for_user(user).access_token)},
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = "username"
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        url_path="me",
        permission_classes=(permissions.IsAuthenticated,)
    )
    def profile(self, request):
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenreViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdminOrReadOnly, ]


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdminOrReadOnly, ]


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year', 'name')

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return TitleWriteSerializer
        return TitleReadSerializer

    def get_queryset(self):
        queryset = Title.objects.all()
        # для ревьюера - не могу их \/ запихнуть в филтерсет филд.
        # работают, но не проходят тесты
        genre = self.request.query_params.get('genre')
        category = self.request.query_params.get('category')
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)
        if category is not None:
            queryset = queryset.filter(category__slug=category)
        return queryset
