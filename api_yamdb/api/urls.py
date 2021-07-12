from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views

from .views import EmailViewSet

router = DefaultRouter()
router.register('auth/email', EmailViewSet, basename='email_post')

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
