import datetime as dt

import jwt
from rest_framework import mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg, FloatField
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404

from .filters import TitlesFilter
from .models import Categories, Genres, Titles, User, Reviews
from .permissions import (
    IsAdmin, IsAuthor, IsModerator, IsSafeMethod, HasUsernameForPOST
)
from .serializers import (
    CategoriesSerializer, GenresSerializer, SendConfirmCodeSerializer,
    TitlesSafeMethodSerializer, TitlesUnSafeMethodSerializer,
    TokenReceiveSerializer, UserSerializer, CommentsSerializer,
    ReviewsSerializer
)

MAIL_SUBJECT = 'Код подтверждения'


class SendConfirmCodeView(APIView):
    permission_classes = (AllowAny,)
    throttle_scope = 'auth-non-employee'

    def create_jwt(self, email):
        """
        Create and sign a confirmation_code like a JSON Web Token.
        Payload is an email and an expiration time.
        """
        secret_key = settings.SECRET_KEY
        expire = dt.datetime.utcnow() + settings.EMAIL_EXPIRATION_TIME
        payload = {'email': email, 'exp': expire}
        signed_token = jwt.encode(payload=payload, key=secret_key,
                                  algorithm='HS256')
        return signed_token

    def post(self, request):
        serializer = SendConfirmCodeSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            signed_code = self.create_jwt(email)
            send_mail(subject=MAIL_SUBJECT, from_email=None,
                      message=signed_code, recipient_list=(email,),
                      fail_silently=True)

            return Response(serializer.validated_data,
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenReceiveView(APIView):
    permission_classes = (AllowAny,)
    throttle_scope = 'auth-non-employee'

    def post(self, request):
        serializer = TokenReceiveSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
        else:
            user = User.objects.create_user(email=email, role='user')

        access = str(AccessToken.for_user(user))

        return Response({'token': access}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.exclude(username__isnull=True)
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    search_fields = ('username',)
    lookup_field = 'username'


class UserMeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get', 'patch')
    throttle_scope = 'burst-non-employee'

    def get_object(self):
        user = get_object_or_404(User, pk=self.request.user.id)
        return user


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    throttle_scope = 'burst-non-employee'
    permission_classes = (
        IsAdmin | IsModerator | IsAuthor | IsSafeMethod, HasUsernameForPOST
    )

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        return title.reviews.all().order_by('-id')

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    throttle_scope = 'burst-non-employee'
    permission_classes = (
        IsAdmin | IsModerator | IsAuthor | IsSafeMethod, HasUsernameForPOST
    )

    def get_queryset(self):
        review = get_object_or_404(Reviews, id=self.kwargs.get('review_id'))
        return review.comments.all().order_by('-id')

    def perform_create(self, serializer):
        review = get_object_or_404(Reviews, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = (IsAdmin | IsSafeMethod,)
    throttle_scope = 'burst-non-employee'
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoriesViewSet(CreateListDestroyViewSet):
    queryset = Categories.objects.all().order_by('name')
    serializer_class = CategoriesSerializer


class GenresViewSet(CreateListDestroyViewSet):
    queryset = Genres.objects.all().order_by('name')
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    class RoundTo(Round):
        arity = 2
        output_field = FloatField()

    queryset = Titles.objects.annotate(
        rating=RoundTo(Avg('reviews__score'), 2)
    ).order_by('-id')
    permission_classes = (IsAdmin | IsSafeMethod,)
    throttle_scope = 'burst-non-employee'
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesSafeMethodSerializer
        return TitlesUnSafeMethodSerializer
