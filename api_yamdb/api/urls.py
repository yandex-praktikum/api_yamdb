from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import SendConfirmCodeView, TokenReceiveView, UserViewSet, \
    ReviewsViewSet, CommentsViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/auth/token/', TokenReceiveView.as_view(),
         name='token_receive_view'),
    path('v1/auth/email/', SendConfirmCodeView.as_view(),
         name='send_confirm_code_view'),
    path('v1/', include(router_v1.urls)),
]
