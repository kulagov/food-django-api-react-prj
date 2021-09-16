from django.db import models
from django.db.models import constraints
from users.models import User


class Ingredient(models.Model):
    name = models.CharField('name', max_length=50)
    measurement_unit = models.CharField('measurement unit', max_length=50)

    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}'


# class Tag(models.Model):
#     # name
#     # colour
#     # slug
#     pass


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


