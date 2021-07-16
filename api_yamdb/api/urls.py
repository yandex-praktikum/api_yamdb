from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, CommentViewSet, EmailViewSet,
                    GenresViewSet, ReviewViewSet, TitlesViewSet,
                    TokenObtainPairView, UserViewSet)

router = DefaultRouter()
router.register('auth/email', EmailViewSet, basename='email_post')
router.register('users', UserViewSet, basename='users')
router.register('categories', CategoriesViewSet, basename='category')
router.register('genres', GenresViewSet, basename='genre')
router.register('titles', TitlesViewSet, basename='title')
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
        TokenObtainPairView.as_view(),
        name="jwt-create"
    ),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', include(jwt)),
]
