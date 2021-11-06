from django.urls import include, path
from djoser import views

from .views import FollowView, FollowViewList

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
    path('auth/token/login/', views.TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', views.TokenDestroyView.as_view(),
         name='logout'),
    path('', include('djoser.urls')),
]
