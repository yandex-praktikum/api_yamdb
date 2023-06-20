from django.urls import path
from rest_framework.authtoken import views
from users.views import UserViewSet, signup_post, token_post

app_name = 'users'

urlpatterns = [
    path('signup/', signup_post),
    path('token/', token_post),
]
