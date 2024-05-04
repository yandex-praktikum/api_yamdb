from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import (TokenObtainView, UserSelfRetrieveUpdateAPIView,
                         UserSignupView, UserViewSet)

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register(r'titles', TitleViewSet, basename='title')
router_v1.register(r'categories', CategoryViewSet, basename='category')
router_v1.register(r'genres', GenreViewSet, basename='genre')

urlpatterns = [
    path(
        'v1/users/me/',
        UserSelfRetrieveUpdateAPIView.as_view(),
        name='user_self'
    ),
    path(
        'v1/auth/signup/',
        UserSignupView.as_view(),
        name='user_signup'
    ),
    path(
        'v1/auth/token/',
        TokenObtainView.as_view(),
        name='token_obtain'
    ),
    path('v1/', include(router_v1.urls)),
]
