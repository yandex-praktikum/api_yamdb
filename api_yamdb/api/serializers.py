from rest_framework import serializers

from api_yamdb.settings import REGEX_SLUG
from reviews.models import (Categories,
                            Genres,
                            Titles,
                            Reviews,
                            Comments)
from rest_framework.validators import UniqueTogetherValidator



class CategoriesSerializer(serializers.ModelSerializer):
    name = serializers.RegexField(regex=REGEX_SLUG,
                                  max_length=256,
                                  required=True)
    slug = serializers.CharField(max_length=50, required=True)

    class Meta:
        exclude = ('id',)
        model = Categories
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    name = serializers.RegexField(regex=REGEX_SLUG,
                                  max_length=256,
                                  required=True)
    slug = serializers.CharField(max_length=50, required=True)

    class Meta:
        exclude = ('id',)
        model = Genres
        lookup_field = 'slug'


class TitlesGetSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Title при GET запросах."""

    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Titles
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class TitlesSerializer(serializers.ModelSerializer):
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

    def to_representation(self, title):
        """Определяет какой сериализатор будет использоваться для чтения."""
        serializer = TitlesGetSerializer(title)
        return serializer.data


class TitleGenreSerializer(serializers.ModelSerializer):
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
