from rest_framework import serializers

from .models import User, Genres, Titles, Categories


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'username', 'email', 'role', 'description', 'first_name', 'last_name')
        read_only_fields = ('id', 'role', 'description', 'first_name', 'last_name')
        model = User


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email',)
        model = User

class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genres

class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Categories

class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all())
    class Meta:
        fields = '__all__'
        model = Titles                        
