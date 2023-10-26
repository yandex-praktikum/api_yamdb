from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, status, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Category, Genre, Title
from users.models import User

from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          SignUpSerializer, TitleSerializer, UserSerializer)


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Title."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category', 'genre', 'name', 'year')


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для модели User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)
    lookup_field = 'username'


class APISignUpUser(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid()
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        user = User.objects.create(
            username=username,
            email=email
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Регистрация!',
            f'Вот Ваш пароль {confirmation_code}.',
            'yamdb@mail.ru',
            [email,],
            fail_silently=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
