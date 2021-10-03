from django.db.models import fields
from requests.api import request
from requests.models import cookiejar_from_dict
from rest_framework import serializers
from users.models import User
from api.models import Tag, Favorite, Recipe, Follow, Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.SerializerMethodField()
    
    class Meta:
        model = Ingredient
        fields = "__all__"
    
    def get_measurement_unit(self, obj):
        return obj.get_measurement_unit_display()


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        qs = Follow.objects.filter(author=obj, user=request.user)
        return qs.exists()
    
    def get_recipes_count(self, obj):
        return obj.recipes.count()
    
    
    class Meta:
        model = User
        fields = ('email', 'id', 'first_name', 'last_name')
    
    
