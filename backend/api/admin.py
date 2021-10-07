from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    search_fields = ("name",)
    list_filter = ("name", "author", "tags")
    empty_value_display = "-пусто-"

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
