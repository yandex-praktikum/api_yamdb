from rest_framework import serializers
from reviews.models import Genre, Category, Title, Review
from rest_framework.relations import SlugRelatedField
from django.db.models import Avg


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
    reviews = ReviewSerializer()
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
