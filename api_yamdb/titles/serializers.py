from django.contrib.auth import get_user_model
from rest_framework import serializers

from titles.models import Category, Genre, Title

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    """Базовый cериализатор жанров."""

    class Meta:

        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Базовый cериализатор категорий."""

    class Meta:
        """Мета класс категории."""

        model = Category
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор произведений для List и Retrieve."""

    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        """Мета класс произведения."""

        fields = '__all__'
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = ("__all__")


class PostTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class GetTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title
