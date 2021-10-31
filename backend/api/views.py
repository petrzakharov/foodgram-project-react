from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from users.pagination import LargeResultsSetPagination

from .filters import RecipeFilter
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import IsAdminOrAuthorOrReadOnly
from .serializers import (
    CreateRecipeSerializer, FavoriteSerializer, IngredientSerializer,
    RecipeListSerializer, ShoppingCartViewSerializer, TagSerializer,
)


class CustomListRetrieveMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class TagViewSet(CustomListRetrieveMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)


class FavoriteView(APIView):
    """Добавить/удалить рецепт из избранного"""
    def get(self, request, pk=None):
        has_favorite = Favorite.objects.filter(
            user=request.user, recipe_id=pk
        ).exists()
        if has_favorite:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(user=request.user, recipe_id=pk)

        # здесь создается объект модели Favorite, но вернуть необходимо Recipe
        serialized = FavoriteSerializer(
            Recipe.objects.get(id=pk)
        )
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None):
        has_favorite = Favorite.objects.filter(
            user=request.user, recipe_id=pk
        ).exists()
        if not has_favorite:
            return Response(
                data={'errors': 'Рецепт не был добавлен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Favorite.objects.filter(user=request.user, recipe_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(CustomListRetrieveMixin):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [permissions.AllowAny, ]
    search_fields = ['name', ]
    pagination_class = None
    # тут должен быть кастомный фильтр


class IngredientView(generics.RetrieveAPIView):
    """Добавить ингредиент"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [permissions.AllowAny, ]
    search_fields = ['name', ]
    pagination_class = None


class IngredientViewList(generics.ListAPIView):
    """Список ингредиентов"""
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny, ]
    search_fields = ['name', ]
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
    filter_class = RecipeFilter
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
    permission_classes = [IsAdminOrAuthorOrReadOnly,
                          permissions.IsAuthenticated, ]

    def get(self, request, pk, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=pk)
        _, created = ShoppingCart.objects.get_or_create(
            recipe=recipe,
            user=request.user
        )
        if not created:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serialized = ShoppingCartViewSerializer(recipe)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=pk)
        try:
            obj = ShoppingCart.objects.get(recipe=recipe, user=request.user)
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

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
