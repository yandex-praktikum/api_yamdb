from rest_framework import serializers

from .models import YamdbUser


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        source='user.password', required=False, write_only=True)

    class Meta:
        model = YamdbUser
        fields = ('username', 'email', 'password')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Запрещено использовать "me" как имя пользователя.')
        return value


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = YamdbUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Запрещено использовать "me" как имя пользователя.')
        return value


class UserPatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = YamdbUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Запрещено использовать "me" как имя пользователя.')
        return value
