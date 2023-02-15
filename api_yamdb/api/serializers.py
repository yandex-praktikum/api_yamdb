from rest_framework import serializers

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор для пользователей """

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
            'confirmation_code'
        )
        extra_kwargs = {
            'confirmation_code': {'write_only': True}
        }


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=128,
    )
    email = serializers.EmailField(
        max_length=128
    )

    class Meta:
        fields = '__all__'
