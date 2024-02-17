import re

from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import User


class ValidateUsername:
    """Валидаторы для username."""

    def validate_username(self, username):
        pattern = re.compile(r'^[\w.@+-]+')

        if pattern.fullmatch(username) is None:
            raise ValidationError('Некорректные символы в username')
        if username == 'me':
            raise ValidationError('Ник "me" нельзя регистрировать!')
        return username


class UserSerializer(serializers.ModelSerializer, ValidateUsername):
    """Сериализатор модели User"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_role(self, role):
        """Запрещает пользователям изменять себе роль."""
        try:
            if self.instance.role != 'admin':
                return self.instance.role
            return role
        except AttributeError:
            return role


class SignUpSerializer(serializers.Serializer, ValidateUsername):
    """Сериализатор регистрации User"""

    username = serializers.CharField(required=True, max_length=50)
    email = serializers.EmailField(required=True, max_length=50)


class TokenSerializer(serializers.Serializer, ValidateUsername):
    """Сериализатор токена"""

    username = serializers.CharField(required=True, max_length=50)
    confirmation_code = serializers.CharField(required=True)
