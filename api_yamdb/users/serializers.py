from rest_framework import serializers
from django.core.validators import RegexValidator

from users.models import User


class UsernameValidator(RegexValidator):
    regex = r'^[\w.@+-]+$'
    flags = 0


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    def validate_username(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('Никнейм "me" запрещен.')
        return data

    class Meta:
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'userrole')


class MeSerializer(serializers.ModelSerializer):
    userrole = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'userrole')
