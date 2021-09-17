from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import DEFAULT_FROM_EMAIL

from .models import User
from .permissions import IsAdmin
from .serializers import (UserJwtSerializer, UserSerializer,
                          UserSignupSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'

    @action(
        methods=['PATCH'],
        detail=True,
        permission_classes=[permissions.IsAdminUser],
    )
    def perform_update(self, serializer):
        role = serializer.validated_data.get('role', None)
        if role is not None:
            if role == User.ADMIN:
                serializer.save(is_staff=True, is_superuser=True)
            if role == User.MODERATOR:
                serializer.save(is_staff=True, is_superuser=False)
            if role == User.USER:
                serializer.save(is_staff=False, is_superuser=False)
        else:
            serializer.save()

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        name='me',
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        role = request.data.get('role')
        if role is not None and role != user.role:
            return Response(
                {'role': 'user'},
                status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
def signup(request):
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.confirmation_code = default_token_generator.make_token(user)
        mail_subject = 'confirmation code'
        message = f'Your confirmation code: {user.confirmation_code}'
        send_mail(
            mail_subject,
            message,
            DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
            auth_user=user.username,
            )
        return Response(
            {'email': user.email, 'username': user.username},
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = UserJwtSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        user.is_active = True
        user.save()
        token = AccessToken.for_user(user)
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    return Response('Token jwt error', status=status.HTTP_400_BAD_REQUEST)
