from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404

from reviews.models import User, Genre, Category, Title, TitleGenre


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        max_length=150
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        max_length=254
    )

    def validate_username(self, data):
        if data == "me":
            raise serializers.ValidationError("me не может быть использовано "
                                              "в качестве имени пользователя")
        return data

    class Meta:
        fields = ("username", "email")
        model = User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
        max_length=150
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
        max_length=254
    )

    class Meta:
        fields = ("email", "username", "first_name", "last_name", "bio",
                  "role")
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("email", "username", "first_name", "last_name", "bio",
                  "role")
        model = User
        read_only_fields = ('role',)


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

    # def update(self, instance, validated_data):
    #     instance.id = validated_data.get('id', instance.name)
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.year = validated_data.get('year', instance.name)
    #     instance.description = validated_data.get('description', instance.name)
    #     if 'category' in validated_data:
    #         category_slug = validated_data.get('category').get('slug')
    #         instance.category = get_object_or_404(Category, slug=category_slug)
    #     if 'genre' in validated_data:
    #         genres = validated_data.get('genre')
    #         genres_lst = []
    #         for genre in genres:
    #             current_genre, status = Genre.objects.get_or_create(genre)
    #             genres_lst.append(current_genre)
    #         instance.genres.set(genres_lst)
    #     instance.save()
    #     return instance
