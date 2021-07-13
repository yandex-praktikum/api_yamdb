from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views

from .views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

jwt = [
    path(
        '',
        views.TokenObtainPairView.as_view(),
        name="jwt-create"
    ),
    path(
        'refresh/',
        views.TokenRefreshView.as_view(),
        name="jwt-refresh"
    ),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/token/', include(jwt)),
]
