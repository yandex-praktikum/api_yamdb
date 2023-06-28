from django.core.validators import MaxLengthValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator

from api_yamdb.const import MAX_LENGHT_NAME, MAX_USER_NAMES
from api_yamdb.settings import REGEX_SLUG, REGEX_STR
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class SignUpSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=REGEX_STR, max_length=MAX_USER_NAMES, required=True
    )
    email = serializers.EmailField(max_length=254, required=True)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('Никнейм "me" запрещен.')
        if not User.objects.filter(username=data['username'],
                                   email=data['email']):
            if User.objects.filter(username=data['username']):
                raise serializers.ValidationError(
                    'Пользователь с таким никмом уже существует.')
            if User.objects.filter(email=data['email']):
                raise serializers.ValidationError(
                    'Пользователь с таким e-mail уже существует.')
        return data

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=REGEX_STR, max_length=MAX_USER_NAMES, required=True
    )
    confirmation_code = serializers.CharField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=MAX_LENGHT_NAME,)
    slug = serializers.RegexField(
        regex=REGEX_SLUG,
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
    name = serializers.CharField(max_length=MAX_LENGHT_NAME, )
    slug = serializers.RegexField(
        regex=REGEX_SLUG,
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
    # rating = serializers.SerializerMethodField()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )

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
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
