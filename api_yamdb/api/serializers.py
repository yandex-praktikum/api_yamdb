import datetime as dt

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Genre, Title, Review, Comment
from django.forms import ValidationError


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
        

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
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
                'Можно cделать только один отзыв'
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
