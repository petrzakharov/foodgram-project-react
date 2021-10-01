from django.contrib import admin
from django.urls import path, include
from .views import UserCreateView
from rest_framework.routers import DefaultRouter
from .views import TagListView, TagView
#router_v1 = DefaultRouter()
#router_v1.register('users', UserCreateView, basename='user_create')

urlpatterns = [
    path('tags/', TagListView.as_view()),
    path('tags/<int:pk>', TagView.as_view()),
]
