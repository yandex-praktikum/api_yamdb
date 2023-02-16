from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Title, Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


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
