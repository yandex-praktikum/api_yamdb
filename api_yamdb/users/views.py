import random

from api.permissions import AdminAccess, UserSelfPermission
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets

from .models import YamdbUser
from .serializers import (UserPatchSerializer, UserSerializer,
                          UserSignupSerializer)


class UserRegistrationView(generics.CreateAPIView):
    queryset = YamdbUser.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = (permissions.AllowAny,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = YamdbUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminAccess,)
    lookup_field = 'username'

    def perform_create(self, serializer):
        username = self.request.data['username']
        email = self.request.data['email']
        code = random.randint(1000, 9999)  # Генерация случайного кода
        send_mail(
            subject='Confirmation Code',
            message=f'Your confirmation code is: {code}',
            from_email='from@example.com',
            recipient_list=[email],
            fail_silently=True,
        )
        serializer.save(username=username, email=email)


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (UserSelfPermission,)
    http_method_names = ['get', 'patch']

    def get_object(self):
        username = self.request.user.username
        return get_object_or_404(YamdbUser, username=username)

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserPatchSerializer
        return super().get_serializer_class()
