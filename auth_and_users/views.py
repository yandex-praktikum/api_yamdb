from django.db.models.fields import EmailField
from rest_framework import serializers
from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, CodeSerializer
from rest_framework import status
from django.core.mail import send_mail
from .models import CostumUser
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator


@api_view(['POST'])
def get_code(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        user = get_object_or_404(CostumUser, email=serializer.data['email'])
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'api-registration',
            f'your confirmation_code: {confirmation_code}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        return Response({"code": f"{confirmation_code}"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_token(request):
    serializer = CodeSerializer(data=request.data)
    if serializer.is_valid():
        user_email = serializer.data['email']
        confirmation_code = serializer.data['confirmation_code']
        user = get_object_or_404(CostumUser, email=user_email)
        if default_token_generator.check_token(user, confirmation_code):
            jwt_token_for_user = RefreshToken.for_user(user)
            data = {"token": f"{jwt_token_for_user}"}
            Response(data, status=status.HTTP_200_OK)
        response(status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)