from django.contrib.admin.filters import ChoicesFieldListFilter
from django.db import models

from users.models import User

from .utils import greater_then_zero


class Follow(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                            verbose_name="Подписчик", related_name="followers")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                            verbose_name="На кого подписан",
                            related_name="followings")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "author"],
                                         name="unique_follow"),
        ]

    def __str__(self):
        return str(self.user.username) + '__' + str(self.author.username)


class IngredientAmount(models.Model):
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        blank=False, 
        validators=[greater_then_zero], 
        unique=True
    )
    
    def __str__(self):
        return str(self.amount)


class Ingredient(models.Model):
    UNIT_CHOICES = (
        ("g", "г"),
        ("ml", "мл"),
        ("sht", "шт."),
        ("stl", "ст. л."),
        ("pvks", "по вкусу"),
        ("sheptk", "щепотка"),
        ("kg", "кг"),
        ("chl", "ч. л."),
        ("up", "упаковка"),
        ("st", "стакан"),
    )
    name = models.CharField(
        verbose_name="Ингредиент",
        max_length=50, 
        blank=False, 
        db_index=True, 
        unique=True
    )
    measurement_unit = models.CharField(
        verbose_name="Единицы измерения",
        max_length=30, 
        choices=UNIT_CHOICES, 
        blank=False
    )
    
    def __str__(self):
        return self.name + '__' + self.measurement_unit


class Tag(models.Model):
    name = models.CharField(
        verbose_name="Тег",
        blank=False, 
        max_length=50, 
        unique=True
    )
    color = models.CharField(
        verbose_name="HEX код", 
        blank=False, 
        unique=True,
        max_length=100
    )
    slug = models.SlugField(blank=False, unique=True, db_index=True)
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name="Автор", 
        related_name="recipes", 
        blank=False,
        db_index=True
    )
    name = models.CharField(
        verbose_name="Рецепт", 
        blank=False, 
        max_length=150,
        db_index=True
    )
    image = models.ImageField( 
        upload_to="api/", 
        height_field=None, 
        width_field=None, 
        max_length=None,
        blank=True,
        null=True
    )
    text = models.TextField(
        verbose_name="Описание", 
        blank=False, 
        max_length=255
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name="recipes", blank=False
    )
    tags = models.ManyToManyField(
        Tag, 
        blank=False,
        related_name="recipes"
    )
    cooking_time = models.PositiveSmallIntegerField(
        blank=False, validators=[greater_then_zero]
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации", 
        auto_now_add=True,
        blank=False
    )
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-pub_date",]


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name="Пользователь", 
                             related_name="favorites"
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name="Рецепт", 
                               related_name="favorites"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "recipe"],
                                    name="unique_favorite_recipe"),
        ]
        

    def __str__(self):
        return str(self.user) + '__' + str(self.recipe)


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, 
                             verbose_name="Пользователь", 
                             on_delete=models.CASCADE,
                             related_name="shopping_cart_recipes"
    )
    recipe = models.ForeignKey(Recipe,
                               verbose_name="Рецепт",
                               on_delete=models.CASCADE,
                               related_name="shopping_cart_recipes"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "recipe"],
                                    name="unique_recipe_in_cart"),
        ]
