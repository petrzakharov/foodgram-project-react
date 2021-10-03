from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagListView, TagView, FavoriteView, IngredientViewList, IngredientView, FavoriteView


router_v1 = DefaultRouter()
router_v1.register('favorite', FavoriteView, basename='favorite')


urlpatterns = [
    path('tags/', TagListView.as_view()),
    path('tags/<int:pk>/', TagView.as_view()),
    path('ingredients/<int:pk>/', IngredientView.as_view()),
    path('ingredients/', IngredientViewList.as_view()),
    path('recipes/<int:pk>/favorite/', FavoriteView.as_view()),
]
