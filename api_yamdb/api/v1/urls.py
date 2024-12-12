from django.urls import include, path
from rest_framework import routers

from v1.views import CategoryViewSet, GenreViewSet, TitleViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('users', UserViewSet, basename='user')
router.register('titles', TitleViewSet, basename='title')


urlpatterns = [
    path('', include(router.urls)),
]
