import datetime as dt

from django.db.models import Avg
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from core import constants as const
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(min_value=const.RATING_MIN_VALUE,
                                      max_value=const.RATING_MAX_VALUE,
                                      read_only=True,
                                      allow_null=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'rating', 'genre', 'category',
        )


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
        allow_empty=False,
        allow_null=False
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    year = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category',
        )

    def validate_year(self, value):
        current_year = dt.datetime.today().year
        if not (value <= current_year):
            raise serializers.ValidationError(
                const.MESSAGE_VALIDATION_YEAR_ERROR)
        return value

    def to_representation(self, instance):
        serializer = TitleReadSerializer(instance)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    text = serializers.CharField()
    score = serializers.IntegerField(
        max_value=10,
        min_value=0
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (request.method == 'POST' and Review.objects.filter(
                author=request.user, title=title).exists()):
            raise ValidationError(
                'Можно сделать только один отзыв на произведение!'
            )
        return data


class CommentSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', )
