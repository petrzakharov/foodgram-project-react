from django.db.models import fields
from rest_framework import serializers
from users.models import User
from djoser.serializers import UserCreateSerializer
from api.models import Follow, Favorite, Recipe
from api.serializers import FavoriteSerializer


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('first_name','last_name','username','email','password')




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
        serialized = FavoriteSerializer(qs, many=True)
        return serialized.data
    
    class Meta:
        model = User
        fields = ('email', 'id', 'first_name',
                  'last_name', 'username', 'is_subscribed',
                  'recipes_count', 'recipes')
    
    
