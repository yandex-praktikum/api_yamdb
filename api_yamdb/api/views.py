import random

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .serializers import SignUpSerializer, TokenSerializer


class SignupViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов класса User."""

    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        """Создает и отправляет на почту код подтверждения."""

        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = random.randint(1000, 9999)
        user = User(
            **serializer.validated_data,
            confirmation_code=confirmation_code
        )
        user.save()

        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтвержения: {confirmation_code}',
            from_email='yamdb@yandex.ru',
            recipient_list=[user.email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserTokenViewSet(viewsets.ModelViewSet):
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

        if confirmation_code != user.confirmation_code:
            message = {'confirmation_code': 'Код подтверждения невалиден'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}

        return Response(
            {'token': str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK
        )
