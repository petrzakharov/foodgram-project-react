from django.db.models import fields
from requests.api import request
from requests.models import cookiejar_from_dict
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from api.models import IngredientAmount, ShoppingCart
from users.serializers import CustomUserSerializer
from users.models import User
from api.models import Tag, Favorite, Recipe, Follow, Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.SerializerMethodField()
    
    class Meta:
        model = Ingredient
        fields = "__all__"
    
    def get_measurement_unit(self, obj):
        return obj.get_measurement_unit_display()



class RecipeJoinIngredientsSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer()
    
    class Meta:
        model = IngredientAmount
        exclude = ('recipe',)


class RecipeSerializerList(serializers.ModelSerializer):
    
    author = CustomUserSerializer()
    tags = TagSerializer(many=True)
    ingredients = RecipeJoinIngredientsSerializer(many=True)
    is_favorited = SerializerMethodField()
    is_shopping_cart = SerializerMethodField()
    
    def get_is_favorited(self, obj):
        return Favorite.objects.filter(
            user=self.request.user, recipe=obj.recipe
        ).exists()
    
    def get_is_shopping_cart(self, obj):
        return ShoppingCart.objects.filter(
            user=self.request.user, recipe=obj.recipe
        ).exists()
    
    class Meta:
        model = Recipe
        fields = '__all__'
        

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
