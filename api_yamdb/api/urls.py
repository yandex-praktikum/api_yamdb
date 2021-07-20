from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (CategoriesViewSet, CommentsViewSet, GenresViewSet,
                    ReviewsViewSet, SendConfirmCodeView, TitlesViewSet,
                    TokenReceiveView, UserMeViewSet, UserViewSet)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')
router_v1.register('categories', CategoriesViewSet, basename='categories')
router_v1.register('genres', GenresViewSet, basename='genres')
router_v1.register('titles', TitlesViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/token/', TokenReceiveView.as_view(),
         name='token_receive_view'),
    path('v1/auth/email/', SendConfirmCodeView.as_view(),
         name='send_confirm_code_view'),
    path('v1/users/me/',
         UserMeViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}),
         name='user_me_view_set'),
    path('v1/', include(router_v1.urls)),
]
