from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet, EmailViewSet, CategoriesViewSet,
    GenresViewSet, TitlesViewSet, ReviewViewSet,
    TokenObtainPairView, CommentViewSet
)

router = DefaultRouter()
router.register('auth/email', EmailViewSet, basename='email_post')
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
router.register('users', UserViewSet, basename='users')
router.register('auth/email', EmailViewSet, basename='email')
router.register('categories', CategoriesViewSet, basename='category')
router.register('genres', GenresViewSet, basename='genre')
router.register('titles', TitlesViewSet, basename='title')

jwt = [
    path(
        '',
        TokenObtainPairView.as_view(),
        name="jwt-create"
    ),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', include(jwt)),
]
