from django.urls import include, path
from rest_framework.authtoken import views
from views import UserViewSet

urlpatterns = [
    path('signup/', UserViewSet),
    path('token/', views.obtain_auth_token),
]