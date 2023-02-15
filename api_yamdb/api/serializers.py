from rest_framework import serializers

from reviews.models import User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "username")

    def validate_username(self, data):
        if data == "me":
            raise serializers.ValidationError("me не может быть использовано "
                                              "в качестве имени пользователя")
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "bio",
                  "role")

    def validate_username(self, data):
        if data == "me":
            raise serializers.ValidationError("me не может быть использовано "
                                              "в качестве имени пользователя")
        return data
