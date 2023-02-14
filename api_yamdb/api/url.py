from django.urls import include, path
from rest_framework import routers

from api.views import (TitleViewSet,
                       CategoryViewSet,
                       GenreViewSet,
                       UserViewSet,
                       ReviewsViewSet,
                       CommentViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'users', UserViewSet)
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<reviews_id>\d+)/comments',
                   CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # path('v1/', include('djoser.urls.jwt')),
]
