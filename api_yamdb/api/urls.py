from django.urls import include, path
from rest_framework import routers
from .views import SignupViewSet, GetUserTokenViewSet


router_v1 = routers.DefaultRouter()

router_v1.register('signup', SignupViewSet, basename='signup')
router_v1.register('token', GetUserTokenViewSet, basename='token')


urlpatterns = [
    path('v1/auth/', include(router_v1.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt'))
]
