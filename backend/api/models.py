from django.contrib.admin.filters import ChoicesFieldListFilter
from django.db import models
from django.utils import timezone
from users.models import User

from .utils import greater_then_zero


class Follow(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='На кого подписан',
        related_name='following'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Кто подписан',
        related_name='follower'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow'),
        ]

    def __str__(self):
        return str(self.user.username) + '__' + str(self.author.username)


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Ингредиент',
        max_length=50,
        blank=False,
        db_index=True,
        unique=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=30
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тег',
        blank=False,
        max_length=50,
        unique=True
    )
    color = models.CharField(
        verbose_name='HEX код',
        blank=False,
        unique=True,
        max_length=100
    )
    slug = models.SlugField(blank=False, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes',
        blank=False,
        db_index=True
    )
    name = models.CharField(
        verbose_name='Рецепт',
        blank=False,
        max_length=150,
        db_index=True
    )
    image = models.ImageField(
        upload_to='api/',
        height_field=None,
        width_field=None,
        max_length=None,
        blank=True,
        null=True
    )
    text = models.TextField(
        verbose_name='Описание',
        blank=False,
        max_length=255
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=False,
    )
    cooking_time = models.PositiveSmallIntegerField(
        blank=False, validators=[greater_then_zero]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        blank=False
    )

    class Meta:
        ordering = ['-pub_date', ]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT,
                                   verbose_name='Ингредиент', null=True)
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        blank=False,
        validators=[greater_then_zero],
        unique=True
    )

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return str(self.amount) + '_' + str(self.ingredient)


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorites'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite_recipe'),
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return str(self.user) + '__' + str(self.recipe)


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Покупка',
        on_delete=models.CASCADE,
        related_name='shopping_cart_recipes'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_recipe_in_cart'),
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return str(self.recipe)
