import datetime as dt

from django.forms import ValidationError
from django.shortcuts import get_object_or_404


from django.db.models import Avg, Count, Max
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )
    name = serializers.CharField(
        max_length=256
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
    name = serializers.CharField(
        max_length=256
    )

    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    name = serializers.CharField(
        max_length=256
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category',
            # rating
        )
        read_only_fields = ('id',)

    def validate_year(self, value):
        current_year = dt.datetime.today().year
        if not (value <= current_year):
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category')
        instance.genre.set(validated_data.get('genre'))
        instance.save()
        return instance


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description',
            'genre', 'category'
        )

    def get_rating(self, obj):
        rating = Review.objects.filter(title_id=obj.id).aggregate(
            Avg('score')
        )['score__avg']
        if rating:
            return round(rating)
        return rating


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
        #  lookup_field Возможно необходимо добавить

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
