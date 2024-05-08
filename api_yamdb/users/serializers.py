from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from core import constants as const

User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=const.USERNAME_MAX_LENGTH,
        validators=[UnicodeUsernameValidator()]
    )
    email = serializers.EmailField(max_length=const.EMAIL_MAX_LENGTH)

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        existing_user = User.objects.filter(
            username=username, email=email).first()
        if existing_user:
            return existing_user
        user = User.objects.create(**validated_data)
        return user

    def validate(self, attrs):
        user_with_username = User.objects.filter(
            username=attrs['username']).first()
        user_with_email = User.objects.filter(email=attrs['email']).first()
        if (user_with_email and not user_with_username):
            raise serializers.ValidationError(
                'Пользователя с таким именем не существует!')
        if (user_with_username and not user_with_email):
            raise serializers.ValidationError(
                'Пользователя с такой почтой не существует!')
        return super().validate(attrs)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Запрещено использовать "me" как имя пользователя!')
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Запрещено использовать "me" как имя пользователя!')
        return value


class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=const.USERNAME_MAX_LENGTH)
    confirmation_code = serializers.CharField(max_length=39)

    def validate(self, data):
        username = data['username']
        confirmation_code = data['confirmation_code']
        user = User.objects.filter(username=username).first()
        if user and not default_token_generator.check_token(
                user, confirmation_code
        ):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения!'})
        return data
