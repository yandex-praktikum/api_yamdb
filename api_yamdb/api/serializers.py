from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User, Genre, Category, Title


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


class TitleGenreSerializer(GenreSerializer):
    def to_internal_value(self, data):
        slug = data
        return {
            'slug': slug,
        }


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = TitleCategorySerializer()

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')
        model = Title
