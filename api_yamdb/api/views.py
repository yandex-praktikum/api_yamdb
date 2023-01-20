from rest_framework import viewsets
from serializers import ReviewSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .permissions import AdminModeratorAuthorPermission



class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get("title_id")
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get("title_id")
        )
        serializer.save(author=self.request.user, title=title)