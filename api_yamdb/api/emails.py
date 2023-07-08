from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from users.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from .serializers import GetJWTSerializer, SendCodeSerializer, UserEditSerializer, UserSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from .permissions import IsAdmin

from rest_framework.exceptions import ValidationError


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = SendCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if User.objects.filter(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email']).exists():
        user = get_object_or_404(
            User, username=serializer.validated_data['username'],
            email=serializer.validated_data['email']
        )
        if user.last_login is None:
            confirmation_code = default_token_generator.make_token(user)
            send_email(user, confirmation_code)
            return Response(request.data, status=status.HTTP_200_OK)
    user = serializer.save()
    confirmation_code = default_token_generator.make_token(user)
    send_email(user, confirmation_code)
    return Response(serializer.data, status=status.HTTP_200_OK)


def send_email(user, confirmation_code):
    send_mail(
        subject='YaMDb registration',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=None,
        recipient_list=[user.email],
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer = GetJWTSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    serializer = GetJWTSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )

    if default_token_generator.check_token(
        user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdmin])
def create(self, request, *args, **kwargs):
    serializer = UserEditSerializer(data=request.data)
    user = User(
        email=self.validated_data['email'],
        username=self.validated_data['username'],
        first_name=self.validated_data['first_name'],
        last_name=self.validated_data['last_name'],
        bio=self.validated_data['bio'],
        role=self.validated_data['role'],
    )
    user.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
