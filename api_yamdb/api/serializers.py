import datetime as dt

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Genre, Title


class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        # validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        # validators=[UniqueValidator(queryset=Title.objects.all())]
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')  # rating
        read_only_fields = ('id',)  # rating

    def validate_year(self, value):
        current_year = dt.datetime.today().year
        if not (value <= current_year):  # возможно: if value
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        model = Category
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        lookup_field = 'slug'
