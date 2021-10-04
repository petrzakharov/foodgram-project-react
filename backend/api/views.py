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
from .serializers import TagSerializer, FavoriteSerializer, IngredientSerializer
from rest_framework import permissions, filters, status, viewsets
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


# Тег - готово
class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
class TagView(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# Избранное - готово, протестировать, когда будут наполнены рецепты
class FavoriteView(APIView):
    def get(self, request, pk=None):
        has_favorite = Favorite.objects.filter(
            user=request.user, recipe_id=pk
        ).count()
        if has_favorite:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(user=request.user, recipe_id=pk)
        return Response(status=status.HTTP_201_CREATED)


    def delete(self, request, pk=None):
        has_favorite = Favorite.objects.filter(
            user=request.user, recipe_id=pk
        ).count()
        if not has_favorite:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.filter(user=request.user, recipe_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

# Ингредиент - готово
class IngredientView(generics.RetrieveAPIView):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class IngredientViewList(generics.ListAPIView):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name_param = self.request.query_params.get('name')
        if not name_param:
            return queryset
        return queryset.filter(name__startswith=name_param)






