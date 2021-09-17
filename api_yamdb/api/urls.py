from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                           ReviewViewSet, TitlesViewSet)
from users.views import UserViewSet, get_jwt_token, signup

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('genres', GenresViewSet, basename='genres')
router.register('categories', CategoriesViewSet, basename='categories')
router.register('titles', TitlesViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='review_by_post',
)
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comments_by_review',
)
URLS = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_jwt_token, name='token'),
]

URLS += router.urls

urlpatterns = [
    path('v1/', include(URLS)),
]
