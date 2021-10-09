from api.models import (
    Favorite, Follow, Ingredient, IngredientAmount, Recipe, ShoppingCart, Tag,
)
from django.db.models import F, fields
from drf_extra_fields.fields import Base64ImageField
from requests.api import request
from requests.models import cookiejar_from_dict
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.generics import get_object_or_404
from users.models import User
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class ShowRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientToRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


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


class CreateRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = AddIngredientToRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author', )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            obj = get_object_or_404(Ingredient, id=ingredient['id'])
            amount = ingredient['amount']
            if IngredientAmount.objects.filter(
                recipe=recipe,
                ingredient=obj
            ).exists():
                amount += F('amount')
            IngredientAmount.objects.update_or_create(
                recipe=recipe,
                ingredient=obj,
                defaults={'amount': amount}
            )
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in self.initial_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            for ingredient in ingredients:
                IngredientAmount.objects.create(
                    recipe=instance,
                    ingredient=get_object_or_404(
                        Ingredient,
                        id=ingredient['id']
                    ),
                    amount=ingredient['amount']
                )
        if 'tags' in self.initial_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)

        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

    def validate(self, data):
        ingredients = data['ingredients']
        for ingredient in ingredients:
            if ingredient['amount'] <= 0:
                raise serializers.ValidationError(
                    'Увеличьте количество ингридиента'
                )
        return data

    def to_representation(self, instance):
        return RecipeListSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class ShoppingCartViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('name', 'image', 'cooking_time')
