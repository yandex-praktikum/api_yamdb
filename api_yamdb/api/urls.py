from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                    CommentViewSet, ReviewViewSet, UserViewSet,
                    token_post, signup_post)
# Создаётся роутер
router = DefaultRouter()

# Вызываем метод .register с нужными параметрами
router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('titles/(?P<title_id>\\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    'titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments',
    CommentViewSet, basename='comments')


urlpatterns = [path('v1/auth/token/', token_post),
               path('v1/auth/signup/', signup_post),
               path('v1/', include(router.urls)),
               ]
