from rest_framework import serializers
from reviews.models import (Categories,
                            Genres,
                            Titles,
                            Reviews,
                            Comments)

class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий произведений."""
    class Meta:
        exclude = ('id',)
        model = Categories
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров произведений."""
    class Meta:
        exclude = ('id',)
        model = Genres
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для POST-запросов к произведениям."""
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Titles


class TitleGenreSerializer(serializers.ModelSerializer):
    """Сериализатор для GET-запросов к произведениям."""
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Titles


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
