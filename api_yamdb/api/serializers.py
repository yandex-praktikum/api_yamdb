from rest_framework import serializers

from reviews.models import User, Genre, Category, Title


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "username")

    def validate_username(self, data):
        if data == "me":
            raise serializers.ValidationError("me не может быть использовано "
                                              "в качестве имени пользователя")
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "bio",
                  "role")

    def validate_username(self, data):
        if data == "me":
            raise serializers.ValidationError("me не может быть использовано "
                                              "в качестве имени пользователя")
        return data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), many=True, slug_field="slug"
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
