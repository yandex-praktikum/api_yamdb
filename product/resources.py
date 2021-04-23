from import_export import resources
from .models import Category, Genre, Title


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug',)



class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug',)        


class TitleResource(resources.ModelResource):
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category') 