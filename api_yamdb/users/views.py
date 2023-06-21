# import uuid

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import YAMDB
from users.models import User
from users.permissions import IsAdminOnly
from users.serializers import (SignUpSerializer,
                               TokenSerializer, UserSerializer)


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """Вьюсет для создания пользователей."""
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        """Создает объект класса User и
        отправляет на почту пользователя код подтверждения."""
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # email = serializer.validated_data['email']
        # username = serializer.validated_data['username']
        try:
#             user, _ = User.objects.get_or_create(username=username,
#                                                  email=email)
           user, _ = User.objects.get_or_create(**serializer.validated_data)
        except IntegrityError:
            return Response('Такой логин или email уже существуют',
                            status=status.HTTP_400_BAD_REQUEST)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения Yamdb',
            message=f'Код подтверждения: {confirmation_code}',
            from_email=YAMDB,
            email=user.email,
            confirmation_code=confirmation_code
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TokenViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """Вьюсет для получения токена."""
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
            message = {'confirmation_code': 'Неверный код подтверждения.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
#    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOnly, )
    filter_backends = (filters.SearchFilter, )
    filterset_fields = ('username')
    search_fields = ('username', )
    lookup_field = 'username'
    http_method_names = ['get', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w.@+-]+\Z$)',
        url_name='get_user',
        permission_classes=(IsAdminOnly, )
    )
    def get_change_user_by_username(self, request, username):
        """Обеспечивает получание данных пользователя по его username и
        управление ими."""
        user = get_object_or_404(User, username=username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # elif request.method == 'PUT':
        #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_patch_me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def signup_post(request):
#     # serializer = SignUpSerializer(data=request.data)
#     # serializer.is_valid(raise_exception=True)
#     # email = serializer.validated_data['email']
#     # username = serializer.validated_data['username']
#     try:
#         user, create = User.objects.get_or_create(
#             username=username,
#             email=email
#         )
#     except IntegrityError:
#         return Response(
#             'Такой логин или email уже существуют',
#             status=status.HTTP_400_BAD_REQUEST
#         )
#     confirmation_code = str(uuid.uuid4())
#     user.confirmation_code = confirmation_code
#     user.save()
#     send_mail(
#         'Код подверждения', confirmation_code,
#         ['admin@email.com'], (email,), fail_silently=False
#     )
#     return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def token_post(request):
#     serializer = TokenSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     username = serializer.validated_data['username']
#     confirmation_code = serializer.validated_data['confirmation_code']
#     user_base = get_object_or_404(User, username=username)
#     if confirmation_code == user_base.confirmation_code:
#         token = str(AccessToken.for_user(user_base))
#         return Response({'token': token}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request):
    #     user = get_object_or_404(User, username=self.request.user)
    #     if request.method == 'GET':
    #         if request.user.role == 'admin':
    #             serializer = UserSerializer(user)
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(request.user.role, status=status.HTTP_403_FORBIDDEN)

    # def put(self, request):
    #     if request.method == 'PUT':
    #         serializer = UserSerializer(user)
    #         return Response(serializer.data,
    #                         status=status.HTTP_405_METHOD_NOT_ALLOWED)
    # @action(
    #     methods=['get', 'patch', ],
    #     detail=False,
    #     url_path='me',
    #     permission_classes=(IsAuthorOrAdmins, IsAdminOnly)
    # )
    # def get_patch_me(self, request):
    #     user = get_object_or_404(User, username=self.request.user)
    #     if request.method == 'GET':
    #         serializer = MeSerializer(user)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     if request.method == 'PATCH':
    #         serializer = MeSerializer(user,
    #                                   data=request.data,
    #                                   partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)

        # if request.method == 'PUT':
        #     serializer = UserSerializer(user)
        #     return Response(serializer.data,
        #                     status=status.HTTP_405_METHOD_NOT_ALLOWED)
