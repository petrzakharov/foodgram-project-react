from django.db.models import fields
from rest_framework import serializers
from users.models import User
from djoser.serializers import UserCreateSerializer, UserSerializer
from api.models import Follow, Favorite, Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta():
        model = User
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=self.context['request'].user,
                                     author=obj).exists()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        qs = Follow.objects.filter(author=obj, user=request.user)
        return qs.exists()
    
    def get_recipes_count(self, obj):
        return obj.recipes.count()
    
    def get_recipes(self, obj):
        request = self.context.get('request')
        qs = obj.recipes.all()[:request.query_params.get('recipes_limit')]
        serialized = RecipeSerializer(qs, many=True)
        return serialized.data
    
    class Meta:
        model = User
        fields = ('email', 'id', 'first_name',
                  'last_name', 'username', 'is_subscribed',
                  'recipes_count', 'recipes')
    
