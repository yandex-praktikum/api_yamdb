from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (GetTokenView, RegistrationView, CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UserViewSet)

app_name = 'api'

router = SimpleRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    'users',
    UserViewSet,
    basename='users'
)
router.register(
    'categories',
    CategoryViewSet,
    basename='сategories'
)
router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', RegistrationView, name='register'),
    path('v1/auth/token/', GetTokenView, name='token'),
]
