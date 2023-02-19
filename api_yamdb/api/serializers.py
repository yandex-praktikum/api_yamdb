
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from reviews.models import User, Genre, Category, Title, TitleGenre, Review, Comment


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "username")

    def validate_username(self, data):
        if data == "me":
            raise serializers.ValidationError("me не может быть использовано "
                                              "в качестве имени пользователя")
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "bio",
                  "role")

    def validate_username(self, data):
        if data == "me":
            raise serializers.ValidationError("me не может быть использовано "
                                              "в качестве имени пользователя")
        return data

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleGenreSerializer(serializers.ModelSerializer):
    # slug = serializers.SlugRelatedField(slug_field='slug')
    class Meta:
        fields = ('slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleCategorySerializer(CategorySerializer):
    def to_internal_value(self, data):
        slug = data
        return {
            'slug': slug,
        }


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = TitleCategorySerializer()
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), many=True, slug_field="slug"
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        category_slug = validated_data.pop('category').get('slug')
        category = get_object_or_404(Category, slug=category_slug)
        title = Title.objects.create(category=category, **validated_data)
        title.save()
        for each in genres:
            genre = Genre.objects.get(name=each)
            TitleGenre.objects.get_or_create(title=title, genre=genre)
        return title


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Можно оставить только один отзыв!')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
