from django.urls import path
from . import views

urlpatterns = [
    path('email/', views.get_code),
    path('token/', views.get_token),
    #ath('', ),
    #path('/<str:username>', ),
]
