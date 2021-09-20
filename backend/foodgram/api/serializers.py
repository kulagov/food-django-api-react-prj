from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from users.models import Follow
from users.serializers import UserSerializer

from .models import Component, Ingredient, Recipe, Tag


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
    name = serializers.StringRelatedField(
        read_only=True,
        source='ingredient'
    )
    measurement_unit = serializers.StringRelatedField(
        read_only=True,
        source='ingredient'
    )

    class Meta:
        model = Component
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = ComponentSerializer(many=True, source='components')

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            # 'is_favorited',
            # 'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    # def get_is_favorited(self, obj):
    #     user = self.context.get('request').user
    #     return Follow.objects.filter(user=user, following=obj).exists()

    def create(self, validated_data):
        ingredients = validated_data.pop('components')
        tags = self.initial_data['tags']
        user = self.context['request'].user
        recipe = Recipe.objects.create(**validated_data, author=user)

        for ingredient in ingredients:
            Component.objects.create(
                recipe=recipe,
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            )
        for tag in tags:
            recipe.tags.add(Tag.objects.get(id=tag['id']))
        return recipe
