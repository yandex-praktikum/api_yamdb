from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet,
                    CommentViewSet,
                    GenreViewSet,
                    ReviewViewSet,
                    TitleViewSet,
                    UserViewSet)

router = DefaultRouter()

router.register(r'categories', CategoryViewSet)  # Все поинты от Варвары
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/',
    ReviewViewSet, basename='reviews')  # кроме этого,это мой
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')  # и этого
router.register(r"users", UserViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
