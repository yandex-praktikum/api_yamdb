from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User
from .permissions import IsAdmin
from .sendtoken import make_token
from .serializers import RegisterSerializer, TokenSerializer, UserSerializer


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
