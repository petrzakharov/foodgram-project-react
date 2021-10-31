from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from .views import FollowView, FollowViewList, UserActivationView

urlpatterns = [
    path(
        'users/subscriptions/',
        FollowViewList.as_view(),
        name='subsriptions'
    ),
    path(
        'users/<int:pk>/subscribe/',
        FollowView.as_view(),
        name='subscribe'
    ),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'activation/<str:uid>/<str:token>/',
        UserActivationView.as_view(),
        name='activation'
    ),
]
