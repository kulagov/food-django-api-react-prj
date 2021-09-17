from django.db import models
from django.db.models import constraints
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

# class Recipe(models.Model):
#     # author
#     # name
#     # image
#     # description
#     # Tag many
#     # Cooking_time
#     pass


# class Component(models.Model):
#     # recipe foreign
#     # ingredient manytomany
#     # ammount


# class ShoppingList(models.Model):
#     # user
#     # recipe


