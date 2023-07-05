from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User
from .serializers import CategoriesSerializer, GenresSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User
        
class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre
        lookup_field = 'slug'


  
class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.RegexField(regex=r'^[\w.@+-]+$', required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        if username == 'me':
            raise serializers.ValidationError("This name cannot be used")
        return attrs
   
 
class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        exclude = ('review',)
        read_only_fields = ('review', 'pub_date')


class TitlesGetSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ['id', 'name', 'category', 'genre', 'rating']


class TitlesPostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = ['id', 'name', 'category', 'genre', 'rating']

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        genre_data = validated_data.pop('genre')
        title = Title.objects.create(category=category_data, **validated_data)
        title.genre.set(genre_data)
        return title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        exclude = ('title',)
        read_only_fields = ('pub_date',)

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method != 'POST':
            return data

        title_id = self.context.get('view').kwargs.get('title_id')
        author = request.user
        review = Review.objects.filter(author=author, title_id=title_id)
        if review.exists():
            raise serializers.ValidationError(
                'You can only post one review.'
            )
        return data
    
class GetJWTSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if username == 'admin':
            raise serializers.ValidationError("Недопустимое имя пользователя")

        return data
