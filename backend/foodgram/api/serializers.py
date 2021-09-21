from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.models import Follow
from users.serializers import UserSerializer

from .models import Component, Ingredient, Recipe, ShoppingList, Tag


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class ShoppingAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


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
    ingredients = ComponentSerializer(many=True, source='components')
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'tags',
            # 'is_favorited',
            'is_in_shopping_cart',
            'image',
            'name',
            'text',
            'cooking_time'
        )
        extra_kwargs = {
            'text': {'required': True},
            'cooking_time': {'required': True},
            # 'image': {'required': True},
        }

    def get_is_in_shopping_cart(self, obj):
        return ShoppingList.objects.filter(
            user=self.context['request'].user,
            recipe=obj
        ).exists()


class ComponentSerializerCreate(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all(),
    )

    class Meta:
        model = Component
        fields = (
            'id',
            'amount'
        )


class RecipeSerializerCreate(serializers.ModelSerializer):
    ingredients = ComponentSerializerCreate(many=True, source='components')

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )
        extra_kwargs = {
            'text': {'required': True},
            'cooking_time': {'required': True},
        }


    def create(self, validated_data):
        ingredients = validated_data.pop('components')
        tags = validated_data.pop('tags')
        user = self.context['request'].user
        recipe = Recipe.objects.create(**validated_data, author=user)

        self.add_tags_and_components(recipe, ingredients, tags)

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('components')
        tags = validated_data.pop('tags')
        user = self.context['request'].user
        if user != instance.author:
            raise serializers.ValidationError('user != author')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.ingredients.clear()
        instance.tags.clear()

        self.add_tags_and_components(instance, ingredients, tags)

        instance.save()
        return instance

    def add_tags_and_components(self, obj, ingredients, tags):
        for ingredient in ingredients:
            Component.objects.create(
                recipe=obj,
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            )
        for tag in tags:
            new_tag = get_object_or_404(Tag, id=tag.id)
            obj.tags.add(new_tag)
