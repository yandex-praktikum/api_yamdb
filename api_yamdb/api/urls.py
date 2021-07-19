from django.urls import include, path
from rest_framework import views
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet,
                    TokenObtainPairView, UserViewSet, CreateNewUser)

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
jwt = [
    path(
        '',
        TokenObtainPairView,
        name="jwt-create"
    ),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', include(jwt)),
    path('v1/auth/email/', CreateNewUser),
]
