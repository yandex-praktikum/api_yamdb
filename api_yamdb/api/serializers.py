from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import User, Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов к произведениям."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        exclude = ('title',)
        read_only_fields = ('pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев к отзывам."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        exclude = ('review',)
        read_only_fields = ('pub_date',)


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
