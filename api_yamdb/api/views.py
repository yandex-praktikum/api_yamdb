from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)

from api.models import Title
from api.permissions import (IsAuthorOrStuffOrReadOnly,)
from api.serializers import (ReviewSerializer,)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorOrStuffOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
