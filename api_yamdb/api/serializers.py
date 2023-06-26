from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from django.core.validators import MaxLengthValidator

from api_yamdb.settings import REGEX_SLUG
from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256, )
    slug = serializers.RegexField(regex=REGEX_SLUG,
                                  max_length=50, )

    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256, )
    slug = serializers.RegexField(regex=REGEX_SLUG,
                                  max_length=50, )

    class Meta:
        exclude = ('id',)
        model = Genre
        lookup_field = 'slug'


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Title при GET запросах."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        fields = '__all__'
        model = Title

    def to_representation(self, title):
        """Определяет какой сериализатор будет использоваться для чтения."""
        serializer = TitleGetSerializer(title)
        return serializer.data


class TitleGenreSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    # title = serializers.SlugRelatedField(read_only=True, slug_field='name')
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    def validate_rating(self, value):
        if value > 10 and value < 0:
            raise serializers.ValidationError('Оценка по шкале от 1 до 10')
        return value

    def create(self, validated_data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError('Нельзя дважды оставить ревью')
        return Review.objects.create(**validated_data)

    class Meta:
        fields = '__all__'
        model = Review

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message=('Вы можете оставить только один отзыв')
            )
        ]
    

class CommentSerializer(serializers.ModelSerializer):
    # review = serializers.SlugRelatedField(read_only=True, slug_field='text')
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
