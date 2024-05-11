from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet)
from users.views import TokenObtainView, UserSignupView, UserViewSet

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='user')
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register(r'titles/(?P<title_id>[^/.]+)/reviews',
                   ReviewViewSet, basename='review')
router_v1.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet, basename='comment')

v1_auth_urls = [
    path(
        'signup/',
        UserSignupView.as_view(),
        name='user_signup'
    ),
    path(
        'token/',
        TokenObtainView.as_view(),
        name='token_obtain'
    ),
]

v1_urls = [
    path('', include(router_v1.urls)),
    path('auth/', include(v1_auth_urls)),
]

urlpatterns = [
    path('v1/', include(v1_urls)),
]
