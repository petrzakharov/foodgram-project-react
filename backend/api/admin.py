from django.contrib import admin

from .models import Favorite, IngredientAmount, Ingredient, Follow, ShoppingCart, Tag, Recipe

# Recipe фильтры: название авторы теги, вывод: название и автор, на странице рецепта общее число добавлений ??
# Ingredient фильтр по названию, вывод: название ингредиента и единицы измерения
# Users Добавить фильтр списка по email и имени пользователя.

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author")#, "display_count_favorites")
    search_fields = ("name",)
    list_filter = ("name", "author", "tags")
    empty_value_display = "-пусто-"
    
    # def display_count_favorites(self, obj):
    #     """
    #     Отображение cколько раз рецепт был добавлен в избранное.
    #     Уточнить! Возможно неверно, отображаться должно на странице рецепта в админке.
    #     """
    #     return Favorite.objects.filter(receipt=obj).count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user")


admin.site.register(IngredientAmount)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart)
admin.site.register(Follow)
