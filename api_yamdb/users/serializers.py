from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .models import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH

User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=[UnicodeUsernameValidator(),]
    )
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)

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
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, attrs):
        if (
            User.objects.filter(email=attrs['email']).first()
            and not User.objects.filter(username=attrs['username']).first()
        ):
            raise serializers.ValidationError(
                'Пользователя с таким именем не существует!')
        if (User.objects.filter(username=attrs['username']).first()
                and not User.objects.filter(email=attrs['email']).first()):
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


class UserPatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Запрещено использовать "me" как имя пользователя!')
        return value


class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH)
    confirmation_code = serializers.CharField(max_length=5)

    def validate(self, attrs):
        data = super().validate(attrs)
        username = attrs['username']
        confirmation_code = attrs['confirmation_code']
        user = User.objects.filter(username=username).first()
        if user and user.confirmation_code != confirmation_code:
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения!'})
        return data
