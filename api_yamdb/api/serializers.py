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

# Тесты + Шаблоны для rating


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
    #     #  Возможно добавить .select_related('reviews')
    #     rating = Title.objects.filter(
    #         id=obj.id
    #         ).annotate(Avg('review__score', default=0))
    # # Возможно aggrregate
    #     print(rating)
    #     #return round(rating['rating__avg'])
    #     return

    # def get_rating(self, obj):
    #     rating = Title.objects.filter(
    #         id=obj.id).aggregate(Avg('year'))
    #     return round(rating['year__avg'])


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
