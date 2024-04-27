from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import (UserRegistrationView, UserRetrieveUpdateAPIView,
                         UserViewSet)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/users/me/', UserRetrieveUpdateAPIView.as_view(), name='user_self'),
    path('v1/auth/signup/', UserRegistrationView.as_view(),
         name='user_registration'),
    path('v1/', include(router_v1.urls)),
]
