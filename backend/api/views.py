from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from users.pagination import LargeResultsSetPagination

from .filters import IngredientNameFilter, RecipeFilter
from .models import (
    Favorite, Ingredient, IngredientAmount, Recipe, ShoppingCart, Tag,
)
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
    filter_class = IngredientNameFilter


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
        except ShoppingCart.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        ingredients_list = []
        user_shopping_list = IngredientAmount.objects.filter(
            recipe__shopping_cart_recipes__user=request.user.id).values_list(
                'ingredient__name', 'amount', 'ingredient__measurement_unit')
        all_count_ingredients = user_shopping_list.values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
                total=Sum('amount'))
        for ingredient in all_count_ingredients:
            ingredients_list.append(
                f'{ingredient["ingredient__name"]} - '
                f'{ingredient["total"]} '
                f'{ingredient["ingredient__measurement_unit"]} \n\n'
            )
        response = HttpResponse(
            ingredients_list, 'Content-Type: application/pdf')
        response['Content-Disposition'] = 'attachment; filename="wishlist.pdf"'
        return response
