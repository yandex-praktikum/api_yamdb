from django.urls import include, path
from rest_framework import routers

from .views import (
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet
)


v1_router = routers.DefaultRouter()
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
