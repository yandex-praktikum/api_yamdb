import re
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Genre, Category, Title, User, Review, Comment


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


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'slug'


class TitleGetSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(read_only=True)
    genre = SlugRelatedField(read_only=True, allow_null=True)
    score = ReviewSerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')

        def get_rating(self, obj):
            return Title.objects.annotate(rating=Avg('reviews__score'))


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = ('name', 'year'
                  'description', 'genre', 'category')


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

    def validate_first_name(self, value):
        if len(value) > 150:
            raise serializers.ValidationError(
                'Длина поля не должна быть длинее 150 символов'
            )

    def validate_last_name(self, value):
        if len(value) > 150:
            raise serializers.ValidationError(
                'Длина поля не должна быть длинее 150 символов'
            )


class RegisterSerializer(serializers.Serializer):
    """ Сериализатор для решистрации пользователя """

    username = serializers.CharField(
        max_length=128
    )
    email = serializers.EmailField(
        max_length=128
    )

    class Meta:
        fields = '__all__'

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено'
            )
        pattern = re.compile(r'^[\w.@+-]+')
        if not pattern.match(value):
            raise serializers.ValidationError(
                'Поле username должно соответсвовать паттерну: ^[\w.@+-]+\z'
            )
        return value


class TokenSerializer(serializers.Serializer):
    """
    Сериализатор для отправки проверочного кода
    и получения jwt-токена
    """

    username = serializers.CharField(
        max_length=128,
    )
    confirmation_code = serializers.CharField(
        max_length=50
    )

    class Meta:
        fields = '__all__'
