from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GetTokenView, RegistrationView, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', RegistrationView.as_view(), name='register'),
    path('v1/auth/token/', GetTokenView.as_view(), name='token')
]
