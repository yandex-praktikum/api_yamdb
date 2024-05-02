from api.permissions import AdminAccess, UserSelfAccess
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, views, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .authentication import ConfirmationCodeAuthentication
from .serializers import (CustomTokenObtainSerializer, UserPatchSerializer,
                          UserSerializer, UserSignupSerializer)

User = get_user_model()


class UserSignupView(views.APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                user.send_confirmation_email()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (AdminAccess,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def perform_create(self, serializer):
        username = self.request.data['username']
        email = self.request.data['email']
        serializer.save(username=username, email=email)


class UserSelfRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (UserSelfAccess,)
    http_method_names = ['get', 'patch']

    def get_object(self):
        username = self.request.user.username
        return get_object_or_404(User, username=username)

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserPatchSerializer
        return super().get_serializer_class()


class CustomTokenObtainView(TokenObtainPairView):
    authentication_classes = [ConfirmationCodeAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            confirmation_code = serializer.validated_data.get(
                'confirmation_code')
            user = User.objects.filter(
                username=username, confirmation_code=confirmation_code).first()
            if user:
                refresh = RefreshToken.for_user(user)
                data = {
                    'token': str(refresh.access_token),
                }
                return Response(data)
            else:
                return Response(
                    {'error': 'Неверное имя пользователя'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
