from rest_framework import serializers
from reviews.models import Reviews, Comments
from rest_framework.validators import UniqueTogetherValidator


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
        )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )

    def validate_rating(self, value):
        if value > 10 and value < 0:
            raise serializers.ValidationError('Оценка по шкале от 1 до 10')
        return value

    class Meta:
        fields = '__all__'
        model = Reviews

        validators = [
            UniqueTogetherValidator(
                queryset=Reviews.objects.all(),
                fields=('title', 'author'),
                message=('Вы можете оставить только один отзыв')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='text'
        )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )

    class Meta:
        fields = '__all__'
        model = Comments
