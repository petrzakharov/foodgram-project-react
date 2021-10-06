from django.db.models import query
from django.shortcuts import render
from requests.api import request
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from .models import Ingredient, Tag, Favorite, Follow, Recipe
from users.models import User
from .serializers import RecipeSerializerList, TagSerializer, FavoriteSerializer, IngredientSerializer
from rest_framework import permissions, filters, status, viewsets
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


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


class RecipeView(viewsets.ViewSet):
    queryset = Recipe.objects.all()
    
    def list(self, request):
        serializer = RecipeSerializerList(self.queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        data = RecipeCreateSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        return Response(data.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk):
        pass
    
    def update(self, request, pk=None):
        pass
    
    def destroy(self, request, pk=None):
        pass
    
    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return []
        if self.actions == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            return [] # написать кастомный пермишн на проверку автора
        return [permission() for permission in permission_classes]
