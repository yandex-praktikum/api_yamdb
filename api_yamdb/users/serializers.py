from rest_framework import serializers

from api_yamdb.settings import REGEX_STR
from users.models import User


class SignUpSerializer(serializers.Serializer):
    username = serializers.RegexField(regex=REGEX_STR,
                                      max_length=150,
                                      required=True)
    email = serializers.EmailField(max_length=254,
                                   required=True)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('Никнейм "me" запрещен.')
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Пользователь с таким никмом уже существует.')
        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Пользователь с таким e-mail уже существует.')
        return data

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(regex=REGEX_STR,
                                      max_length=150,
                                      required=True)
    confirmation_code = serializers.CharField(max_length=254,
                                              required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=REGEX_STR,
                                      max_length=150,
                                      required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')

    # def validate_username(self, username):
    #     if username == 'me':
    #         raise serializers.ValidationError(
    #             'Использовать имя me запрещено'
    #         )
    #     return username
