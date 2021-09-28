from django.db import models
from validators import validate_int_field

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Ингредиент',
        max_length=100)
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=50)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тэг',
        max_length=50)
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7)
    slug = models.SlugField(
        verbose_name='slug',
        max_length=50,
        unique=True)

    def __str__(self):
        return f'{self.name} - {self.color}'

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200)
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='images/',
        blank=True
    )
    text = models.TextField(
        verbose_name='Рецепт',
        blank=True)
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        blank=True,
        verbose_name='Тэг')
    cooking_time = models.IntegerField(
        'Время приготовления',
        validators=[validate_int_field],
        default=1
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Component',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )

    def __str__(self):
        return f'{self.name} /{self.author}/'

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Component(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='components'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиенты',
    )
    amount = models.IntegerField(
        validators=[validate_int_field],
        default=1,
        verbose_name='Кол-во'
    )

    class Meta:
        verbose_name = 'Компонент'
        verbose_name_plural = 'Компоненты'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppinglist'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppinglist'
    )

    def __str__(self) -> str:
        return f'{self.user} -{self.recipe}'

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favlist',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favlist',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
