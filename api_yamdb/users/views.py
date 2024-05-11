from django.contrib.auth import get_user_model
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import AdminAccess, UserSelfAccess
from users.serializers import (TokenObtainSerializer, UserSerializer,
                               UserSignupSerializer)

User = get_user_model()


class UserSignupView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.send_confirmation_email(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (permissions.IsAuthenticated, AdminAccess)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(permissions.IsAuthenticated, UserSelfAccess)
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        if request.method == 'GET':
            return Response(serializer.data)
        elif request.method == 'PATCH':
            instance = request.user
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=instance.role)
            return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = User.objects.filter(
            username=username).first()
        if user:
            refresh = RefreshToken.for_user(user)
            data = {'token': str(refresh.access_token), }
            return Response(data)
        else:
            return Response(
                {'username': 'Пользователя с такими именем не существует'},
                status=status.HTTP_404_NOT_FOUND
            )
