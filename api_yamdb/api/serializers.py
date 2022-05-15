from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):
        
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    pass


class ReviewSerializer(serializers.ModelSerializer):
    
    pass


class CommentSerializer(serializers.ModelSerializer):
    
    pass