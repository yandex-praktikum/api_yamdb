import datetime as dt

from django.db.models import Avg, Count, Max
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Genre, Title


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
            'genre', 'category', # rating
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

# Рабочий без rating
# class TitleReadSerializer(serializers.ModelSerializer):
#     genre = GenreSerializer(many=True, read_only=True)
#     category = CategorySerializer(read_only=True)

#     class Meta:
#         model = Title
#         fields = (
#             'id', 'name', 'year', 'description',
#             'genre', 'category'
#         )

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

    # def get_rating(self, obj):
    #     Возможно добавить .select_related('reviews')
    #     rating = Title.objects.filter(
    #         title_id=obj.id
    #         ).annotate(Avg('reviews__score', default=0))  # Возможно aggrregate
    #     print(rating)
    #     return round(rating['rating__avg'])

    def get_rating(self, obj):
        rating = Title.objects.filter(
            id=obj.id).aggregate(Avg('year'))
        return round(rating['year__avg'])
