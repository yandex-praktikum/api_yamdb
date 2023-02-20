from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (GetTokenView, RegistrationView, UserViewSet,
                    CategoryViewSet, GenreViewSet,
                    TitleViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', RegistrationView.as_view(), name='register'),
    path('v1/auth/token/', GetTokenView.as_view(), name='token'),
]
