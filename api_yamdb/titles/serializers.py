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


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category', 'description',
                  'genre', 'pub_date', 'rating')


