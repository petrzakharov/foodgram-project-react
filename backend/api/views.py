from django.db.models import query
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from requests.api import request
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from users.pagination import LargeResultsSetPagination

from .models import Favorite, Follow, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import IsAdminOrAuthorOrReadOnly
from .serializers import (
    CreateRecipeSerializer, FavoriteSerializer, IngredientSerializer,
    RecipeListSerializer, ShoppingCartViewSerializer, TagSerializer,
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
                data={'errors': 'Рецепт не был добавлен'},
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
    serializer_class = CreateRecipeSerializer
    permission_classes = [IsAdminOrAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    # filter_class = RecipeFilter # разобрать, написать
    pagination_class = LargeResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeListSerializer
        return CreateRecipeSerializer


class ShoppingCartView(generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartViewSerializer
    permission_classes = [IsAdminOrAuthorOrReadOnly]

    def get(self, request, pk, *args, **kwargs):
        recipe = Recipe.objects.filter(id=pk).first()
        obj, created = ShoppingCart.objects.get_or_create(
            recipe=recipe,
            user=request.user
        )
        if not created:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serialized = ShoppingCartViewSerializer(recipe)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, *args, **kwargs):
        recipe = Recipe.objects.filter(id=pk).first()
        obj = ShoppingCart.objects.get(recipe=recipe, user=request.user)
        if not obj:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartDownloadView(APIView):
    def get(self, request):
        shopping_cart = request.user.shopping.all()
        shopping_list, result = {}, []
        for shopping in shopping_cart:
            ingredients = shopping.recipe.ingredientamount_set.all()
            for ingredient in ingredients:
                name = ingredient.ingredient.name
                amount = ingredient.amount
                unit = ingredient.ingredient.measurement_unit
                if name not in shopping_list:
                    shopping_list[name] = {
                        'amount': amount,
                        'unit': unit
                    }
                else:
                    shopping_list[name]['amount'] += amount
        for item in shopping_list:
            result.append(
                f'{item}, {shopping_list[item]["unit"]}: '
                f'{shopping_list[item]["amount"]} \n\n'
            )

        response = HttpResponse(result, 'Content-Type: application/pdf')
        response['Content-Disposition'] = 'attachment; filename="wishlist.pdf"'
        return response
