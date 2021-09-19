from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Component, Ingredient, Recipe, Tag
from users.models import Follow


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class ComponentSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all(),
    )
    # ingredient = serializers.StringRelatedField(
    #     read_only=True
    # )

    class Meta:
        model = Component
        fields = (
            'id',
            'ingredient',
            'ammount',
        )
        # fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True, source='tag')
    author = UserSerializer(read_only=True)
    ingredients = ComponentSerializer(many=True)
    # is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',  # add is_fav and is_shop
            # 'is_favorited',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    # def get_is_favorited(self, obj):
    #     user = self.context.get('request').user
    #     return Follow.objects.filter(user=user, following=obj).exists()
