from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import (CustomTokenObtainView, UserSelfRetrieveUpdateAPIView,
                         UserSignupView, UserViewSet)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='user')

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
        CustomTokenObtainView.as_view(),
        name='token_obtain'
    ),
    path('v1/', include(router_v1.urls)),
]
