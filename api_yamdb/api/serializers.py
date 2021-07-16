from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Categories, Comment, Genres, Review, Titles, User


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
        fields = ('first_name', 'last_name', 'username', 'bio',
                  'email', 'role'
                  )
        model = User
        lookup_field = 'username'
        extra_kwargs = {'email': {'required': True}}

        # def get_fields(self, *args, **kwargs):
    #     fields = super(UserSerializer, self).get_fields(*args, **kwargs)
    #     request = self.context.get('request', None)
    #     if request and getattr(request, 'method', None) == "POST":
    #         fields['email'].required = True


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


class TitlesPostSerializer(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all())

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Titles


class TitlesGetSerializer(serializers.ModelSerializer):
    genre = CategoriesSerializer(many=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.FloatField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Titles


class TokenObtainPairSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email', 'confirmation_code')
        model = User

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        user = get_object_or_404(User, email=attrs['email'])
        refresh = self.get_token(user)
        data = {'token': str(refresh.access_token)}
        if user.confirmation_code != attrs['confirmation_code']:
            return "Confirmation code is not correct"
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
