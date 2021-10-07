from django.db.models import query
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from requests.api import request
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from users.pagination import LargeResultsSetPagination

from .models import Favorite, Follow, Ingredient, Recipe, Tag
from .permissions import IsAdminOrAuthorOrReadOnly
from .serializers import (
    FavoriteSerializer, IngredientSerializer, RecipeListSerializer,
    TagSerializer,
)


# Тег - готово
class TagListView(generics.ListAPIView):
    """Список всех тегов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None

    
class TagView(generics.RetrieveAPIView):
    """Добавить новый тег"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


# Избранное - готово
class FavoriteView(APIView):
    """Добавить/удалить рецепт из избранного"""
    def get(self, request, pk=None):
        has_favorite = Favorite.objects.filter(
            user=request.user, recipe_id=pk
        ).count()
        if has_favorite:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(user=request.user, recipe_id=pk)
        
        serialized = FavoriteSerializer(
            Recipe.objects.get(id=pk)
        )
        return Response(serialized.data, status=status.HTTP_201_CREATED)


    def delete(self, request, pk=None):
        has_favorite = Favorite.objects.filter(
            user=request.user, recipe_id=pk
        ).count()
        if not has_favorite:
            return Response(
                data={'errors':'Рецепт не был добавлен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        Favorite.objects.filter(user=request.user, recipe_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

# Ингредиент - готово
class IngredientView(generics.RetrieveAPIView):
    """Добавить ингредиент"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None


class IngredientViewList(generics.ListAPIView):
    """Список ингредиентов"""
    serializer_class = IngredientSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name_param = self.request.query_params.get('name')
        if not name_param:
            return queryset
        return queryset.filter(name__startswith=name_param)


class RecipeView(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
   # serializer_class = CreateRecipeSerializer # разобрать, написать
    permission_classes = [IsAdminOrAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    #filter_class = RecipeFilter # разобрать, написать
    pagination_class = LargeResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeListSerializer 
        #return CreateRecipeSerializer  # разобрать, написать
