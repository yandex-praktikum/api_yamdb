import datetime as dt

import jwt
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import permission_classes

from django.conf import settings
from django.core.mail import send_mail

from .filters import UserFilter
from .models import User, Reviews, Comments, Titles
from .permissions import IsAdmin, IsAuthor, IsModerator, IsReadOnly
from .serializers import (SendConfirmCodeSerializer, TokenReceiveSerializer,
                          UserSerializer, ReviewsSerializer,
                          CommentsSerializer)
from .throttling import NonEmployeeScopedRateThrottle, NonEmployeeRateThrottle

MAIL_SUBJECT = 'Код подтверждения'


class SendConfirmCodeView(APIView):
    permission_classes = (AllowAny,)
    throttle_classes = (NonEmployeeScopedRateThrottle,)
    throttle_scope = 'email-non-employee'

    def create_jwt(self, email):
        """
        Create and sign a confirmation_code like a JSON Web Token.
        Payload is a user_id and an expiration time.
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
    throttle_classes = (NonEmployeeScopedRateThrottle,)
    throttle_scope = 'token-non-employee'

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


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filterset_class = UserFilter


@permission_classes([IsAuthor, IsReadOnly])
class ReviewsViewSet(ModelViewSet):
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('titles_id'))
        return Reviews.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs.get('titles_id'))
        if Reviews.objects.filter(author=self.request.user,
                                  title=title).exist():
            raise ValidationError('Можно оставлять только 1 отзыв')
        serializer.save(author=self.request.user, title=title)


@permission_classes([IsAdmin | IsReadOnly | IsModerator])
class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        review = get_object_or_404(Reviews, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Reviews, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
