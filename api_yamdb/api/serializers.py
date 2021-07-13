from rest_framework import serializers


from .models import User, Genres, Titles, Categories, Rewiew



class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        user = self.context['request'].user
        title = self.context['view'].kwargs.get('title_id')
        if (self.context['request'].method == 'POST'
           and Review.objects.filter(author=user, title=title).exists()):
            raise serializers.ValidationError('Ваш отзыв уже был опубликован')
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 'username', 'email', 'role', 'description',
            'first_name', 'last_name'
        )
        read_only_fields = (
            'id', 'role', 'description', 'first_name', 'last_name'
        )
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
