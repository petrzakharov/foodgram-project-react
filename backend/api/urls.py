from django.contrib import admin
from django.urls import path, include
from .views import UserCreateView
from rest_framework.routers import DefaultRouter

#router_v1 = DefaultRouter()
#router_v1.register('users', UserCreateView, basename='user_create')

urlpatterns = [
    path('users/', UserCreateView.as_view()),
    #path('', include(router_v1.urls)),
]
