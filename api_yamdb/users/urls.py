from django.urls import path

from users.views import UserCreateViewSet, TokenViewSet


app_name = 'users'

urlpatterns = [
    path('signup/', UserCreateViewSet.as_view({'post': 'create'})),
    path('token/', TokenViewSet.as_view({'post': 'create'})),
]
