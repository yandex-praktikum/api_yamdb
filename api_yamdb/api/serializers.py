import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Genre, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Произведение еще не создано.')
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User
        lookup_field = 'username'

        def validate_username(self, value):
            if value == 'me':
                raise serializers.ValidationError(
                    'Нельзя зарегистрироваться под этим именем!'
                )
            return value


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150
    )
    email = serializers.EmailField(
        max_length=254
    )

    class Meta:
        fields = (
            'username',
            'email'
        )
        model = User

        def validate_username(self, value):
            if value == 'me':
                raise serializers.ValidationError(
                    'Нельзя зарегистрироваться под этим именем!'
                )
            return value
