from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Title, Review, Comment
from .models import User
from .utils import generate
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ReviewSerializer,
    CommentSerializer
)
from .permissions import (
    IsAdmin,
    IsModerator,
    IsAuthor,
    IsAuthorOrReadOnly
)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title())

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        title_id = self.kwargs.get("title_id")
        review = get_object_or_404(Review, id=review_id, title=title_id)
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class RegisterAPIView(APIView):
    """ View для регистрации """
    register_serializer = RegisterSerializer
    user_serializer = UserSerializer

    def post(self, request):
        data = self.register_serializer(data=request.data)
        if data.is_valid():
            username = data.validated_data.get('username')
            email = data.validated_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                code = user.confirmation_code
            else:
                code = generate()
                data = {
                    'username': username,
                    'email': email,
                    'confirmation_code': code
                }
                user = self.user_serializer(data=data)
