from rest_framework import serializers
from reviews.models import Reviews, Comments


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
