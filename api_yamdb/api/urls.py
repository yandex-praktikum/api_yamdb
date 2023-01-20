from django.urls import path, include
from rest_framework import routers
from .views import CategoryviewSet, GenreviewSet, TitleviewSet
router = routers.DefaultRouter()

router.register('categories', CategoryviewSet, basename='category')
router.register('genres', GenreviewSet, basename='genre')
router.register('titles', TitleviewSet, basename='title')

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls)),
]
