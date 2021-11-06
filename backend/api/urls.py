from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    FavoriteView, IngredientViewSet, RecipeView, ShoppingCartDownloadView,
    ShoppingCartView, TagViewSet,
)

router = DefaultRouter()
router.register('recipes', RecipeView, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('recipes/download_shopping_cart/',
         ShoppingCartDownloadView.as_view(),
         name='download_shopping_cart'
         ),
    path(
        'recipes/<int:pk>/favorite/',
        FavoriteView.as_view(),
        name='add_to_favorite'
    ),
    path(
        'recipes/<int:pk>/shopping_cart/',
        ShoppingCartView.as_view(),
        name='add_to_shopping_cart'
    ),
    path('', include(router.urls)),
]
