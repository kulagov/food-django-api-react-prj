from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import constraints
from django.utils.translation import gettext_lazy
from users.models import User


class Ingredient(models.Model):
    name = models.CharField('name', max_length=50)
    measurement_unit = models.CharField('measurement unit', max_length=50)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField('name', max_length=50)
    color = models.CharField('color', max_length=7)
    slug = models.SlugField('slug', max_length=50, unique=True)

    def __str__(self):
        return f'{self.name} - {self.color}'


def validate_int_field(value):
    if value < 1:
        raise ValidationError(
            _('Значение должно быть не менее 1'),
            params={'value': value},
        )


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField('name', max_length=200)
    image = models.ImageField(
        'image',
        upload_to='images/',
        blank=True
    )
    text = models.TextField('text', blank=True)
    tag = models.ManyToManyField(Tag, related_name='recipes', blank=True)
    cooking_time = models.IntegerField(
        'cooking time',
        validators=[validate_int_field],
        default=1
    )


class Component(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='components'
    )
    ammount = models.IntegerField(
        validators=[validate_int_field]
    )


# class ShoppingList(models.Model):
#     # user
#     # recipe


