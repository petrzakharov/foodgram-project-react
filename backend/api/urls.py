from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    FavoriteView, IngredientView, IngredientViewList, RecipeView, TagListView,
    TagView,
)

router = DefaultRouter()
router.register('recipes', RecipeView, basename='recipe')

urlpatterns = [
    path('tags/', TagListView.as_view()),
    path('tags/<int:pk>/', TagView.as_view()),
    path('ingredients/<int:pk>/', IngredientView.as_view()),
    path('ingredients/', IngredientViewList.as_view()),
    path('recipes/<int:pk>/favorite/', FavoriteView.as_view()),
    path('', include(router.urls)),
]
