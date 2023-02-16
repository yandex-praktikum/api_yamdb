from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

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
