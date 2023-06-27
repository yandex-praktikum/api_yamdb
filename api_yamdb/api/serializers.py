from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from django.core.validators import MaxLengthValidator

# from api_yamdb.settings import REGEX_SLUG
from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256,)
    # slug = serializers.RegexField(regex=REGEX_SLUG,
    #                               max_length=50, )
    slug = serializers.SlugField(
        validators=(
            UniqueValidator(
                queryset=Category.objects.all(),
                message='Поле slug должно быть уникальным!',
            ),
            MaxLengthValidator(50),
        )
    )

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256, )
    # slug = serializers.RegexField(regex=REGEX_SLUG,
    #                               max_length=50, )
    slug = serializers.SlugField(
        validators=(
            UniqueValidator(
                queryset=Genre.objects.all(),
                message='Поле slug должно быть уникальным!',
            ),
            MaxLengthValidator(50),
        )
    )

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Title при GET запросах."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        # fields = (
        #     'id',
        #     'name',
        #     'year',
        #     'rating',
        #     'description',
        #     'genre',
        #     'category',
        # )
        fields = '__all__'

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj)
        if reviews.count() == 0:
            return None
        else:
            total_score = sum([review.score for review in reviews])
            return round(total_score / reviews.count(), 2)


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'category',
            'genre',
            'description',
        )

    def to_representation(self, title):
        """Определяет какой сериализатор будет использоваться для чтения."""
        serializer = TitleGetSerializer(title)
        return serializer.data


# class TitleGenreSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     genre = GenreSerializer(read_only=True, many=True)
#     rating = serializers.IntegerField(read_only=True)

#     class Meta:
#         fields = '__all__'
#         model = Title


class ReviewSerializer(serializers.ModelSerializer):
    # title = serializers.SlugRelatedField(read_only=True, slug_field='name')
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    # def validate_rating(self, value):
    #     if value > 10 and value < 0:
    #         raise serializers.ValidationError('Оценка по шкале от 1 до 10')
    #     return value

    # def create(self, validated_data):
    #     request = self.context['request']
    #     author = request.user
    #     title_id = self.context['view'].kwargs.get('title_id')
    #     title = get_object_or_404(Title, pk=title_id)
    #     if Review.objects.filter(title=title, author=author).exists():
    #         raise serializers.ValidationError('Нельзя дважды оставить ревью')
    #     return Review.objects.create(**validated_data)

    class Meta:
        # fields = '__all__'
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )

        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=('title', 'author'),
        #         message=('Вы можете оставить только один отзыв')
        #     )
        # ]
    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if Review.objects.filter(title=title, author=author).exists():
            raise ValidationError('Нельзя добавить больше одного отзыва!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    # review = serializers.SlugRelatedField(read_only=True, slug_field='text')
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        # fields = '__all__'
