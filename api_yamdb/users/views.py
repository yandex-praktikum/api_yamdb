from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.db import IntegrityError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status, viewsets, permissions
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdmin
from .models import User
from .serializers import SignUpSerializer, TokenSerializer, UserSerializer


class SignupViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов класса User."""
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        """Создает пользователя и отправляет на почту код подтверждения."""
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(**serializer.validated_data)
        except IntegrityError:
            raise ValidationError(
                'username или email заняты!', status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтвержения: {confirmation_code}',
            from_email='yamdb@yandex.ru',
            recipient_list=[user.email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserTokenViewSet(viewsets.ModelViewSet):
    """Вьюсет выдачи токена пользователям."""
    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        """Предоставляет пользователю JWT токен по коду подтверждения."""
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            message = {'confirmation_code': 'Код подтверждения невалиден'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}

        return Response(
            {'token': str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели User"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)

    @action(
        methods=['get', 'patch'],
        detail=False, url_path='me',
        permission_classes=[permissions.IsAuthenticated,],
        serializer_class=UserSerializer,
    )
    def get_edit_user(self, request):
        """Функция для редактирования своего профиля"""
        user = request.user
        serializer = self.get_serializer(user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
