from rest_framework import serializers
from .models import Category, Genre, Title
# from django.shortcuts import get_object_or_404
# from rest_framework.validators import UniqueTogetherValidator


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        lookup_field = 'slug'
        model = Category
        extra_kwargs = {'name': {'required': True},
        'slug': {'required': False},
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        lookup_field = 'slug'
        model = Genre
        extra_kwargs = {'name': {'required': True},
        'slug': {'required': False},
        }


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title
        # extra_kwargs = {'name': {'required': True},
        # 'slug': {'required': False},
        # }        