from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import Ingredient, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tag',  # change to tags
            'author',
            'ingredients',  # add is_fav and is_shop
            'name',
            'image',
            'text',
            'cooking_time'
        )