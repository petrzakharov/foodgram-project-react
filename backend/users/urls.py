from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserActivationView
from api.views import FollowView

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
    path('activation/<str:uid>/<str:token>/', UserActivationView.as_view()),
    path('subscriptions/', FollowView.as_view()),
]

