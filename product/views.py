from .models import Category, Genre
from .serializers import (CategorySerializer, GenreSerializer)
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

class CategoryViewSet(viewsets.ModelViewSet):
    """ A viewset for viewing and editing post. """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'delete']
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name',]
    
    pagination_class = PageNumberPagination 
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    """ A viewset for viewing and editing post. """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    http_method_names = ['get', 'post', 'delete']
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name',]
    
    pagination_class = PageNumberPagination 
    lookup_field = 'slug'