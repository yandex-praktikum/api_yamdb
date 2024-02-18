from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from titles.models import Title
from users.permissions import OwnerOrReadOnly

from .models import Comment, Review
from .serializers import CommentSerializer, ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для постов."""

    serializer_class = CommentSerializer
    permission_class = OwnerOrReadOnly
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = Review.objects.get(id=self.kwargs.get('review_id'))
        title = Title.objects.get(id=self.kwargs.get('title_id'))
        return Comment.objects.filter(review=review, title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = Review.objects.get(title=title,
                                    id=self.kwargs.get('review_id'))
        serializer.save(title=title, review=review, author=self.request.user)

    def update(self, request, *args, **kwargs):
        return Response({"detail": "PUT method is not allowed."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user and request.user.role == 'user':
            return Response(
                {"detail": "You do not have permission to update a comment."},
                status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user != comment.author and request.user.role == 'user':
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для ревью."""

    serializer_class = ReviewSerializer
    permission_class = OwnerOrReadOnly
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = Title.objects.get(id=self.kwargs.get('title_id'))
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        try:
            title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
            if Review.objects.filter(title=title,
                                     author=self.request.user).exists():
                raise serializers.ValidationError(
                    "You have already reviewed this title.")
            serializer.save(title=title, author=self.request.user)
            title.save()
        except IntegrityError:
            return Response({"detail": "Score must be between 1 and 10"},
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({"detail": "PUT method is not allowed."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author_id != request.user.id and \
           request.user.role == 'user':
            return Response(
                {"detail": "You do not have permission to create a review."},
                status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user != comment.author and request.user.role == 'user':
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)
