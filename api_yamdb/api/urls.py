from django.urls import include, path
from rest_framework import routers
from reviews.views import CommentViewSet, ReviewViewSet
from titles.views import CategoryViewSet, GenreViewSet, TitleViewSet
from users.views import GetUserTokenViewSet, SignupViewSet, UserViewSet

router_auth_v1 = routers.DefaultRouter()
review_router = routers.DefaultRouter()
comment_router = routers.DefaultRouter()


router_auth_v1.register('users', UserViewSet, basename='users')
router_auth_v1.register('genres', GenreViewSet, basename='genres')
router_auth_v1.register('categories', CategoryViewSet, basename='categories')
router_auth_v1.register('titles', TitleViewSet, basename='titles')
review_router.register('reviews', ReviewViewSet, basename='reviews')
comment_router.register('comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('', include(router_auth_v1.urls)),
    path(
        'auth/signup/',
        SignupViewSet.as_view({'post': 'create'}),
        name='signup'
    ),
    path(
        'auth/token/',
        GetUserTokenViewSet.as_view({'post': 'create'}),
        name='token'
    ),
    path('titles/<int:title_id>/', include(review_router.urls)),
    path('titles/<int:title_id>/reviews/<int:review_id>/',
         include(comment_router.urls)),
]
