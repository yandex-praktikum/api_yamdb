from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet,
                       CommentViewSet,
                       GenreViewSet,
                       ReviewViewSet,
                       TitleViewSet)

app_name = 'api'

router = DefaultRouter()

router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/',
    ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
# router.register(r"users", UserViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include('users.urls')),
]
