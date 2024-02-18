from rest_framework import serializers
from titles.serializers import TitleSerializer

from .models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = TitleSerializer(read_only=True)
    pub_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'author', 'title', 'text', 'score', 'pub_date')

    def validate_score(self, value):
        if value > 10 or value < 1:
            raise serializers.ValidationError(
                "Score must be between 1 and 10."
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = TitleSerializer(read_only=True)
    review = ReviewSerializer(read_only=True)
    pub_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'title', 'review', 'text', 'pub_date')
