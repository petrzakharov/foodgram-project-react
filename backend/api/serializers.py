from api.models import (
    Favorite, Follow, Ingredient, IngredientAmount, Recipe, ShoppingCart, Tag,
)
from django.db.models import fields
from requests.api import request
from requests.models import cookiejar_from_dict
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from users.models import User
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ingredient
        fields = "__all__"

    
    
class ShowRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


# class AddIngredientToRecipeSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField()
#     amount = serializers.IntegerField()

#     class Meta:
#         model = Ingredient
#         fields = ('id', 'amount')




class RecipeListSerializer(serializers.ModelSerializer):
    
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = serializers.SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    
    def get_ingredients(self, obj):
        qs = IngredientAmount.objects.filter(recipe=obj)
        return ShowRecipeIngredientSerializer(qs, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:  # проверить что передается request
            return False
        return Favorite.objects.filter(
            recipe=obj, user=request.user
        ).exists()
    
    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous: # проверить что передается request
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj
        ).exists()
    
    class Meta:
        model = Recipe
        exclude = ('pub_date',)
        

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', "cooking_time")
