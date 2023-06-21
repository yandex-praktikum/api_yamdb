from django.urls import path

from users.views import UserCreateViewSet, TokenViewSet


app_name = 'users'

urlpatterns = [
    path('signup/', UserCreateViewSet),
    path('token/', TokenViewSet),
]
