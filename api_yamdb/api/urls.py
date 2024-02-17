from django.urls import include, path
from rest_framework import routers

from users.views import SignupViewSet, GetUserTokenViewSet, UserViewSet


router_auth_v1 = routers.DefaultRouter()

router_auth_v1.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router_auth_v1.urls)),
    path(
        'v1/auth/signup/',
        SignupViewSet.as_view({'post': 'create'}),
        name='signup'
    ),
    path(
        'v1/auth/token/',
        GetUserTokenViewSet.as_view({'post': 'create'}),
        name='token'
    ),
]
