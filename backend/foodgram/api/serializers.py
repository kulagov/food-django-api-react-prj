from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User
from users.serializers import UserSerializer
from api.fields import Base64ImageField
from api.models import (Component, Favorite, Ingredient, Recipe,
                        ShoppingList, Tag)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class ShopAndFavoriteSerializer(serializers.ModelSerializer):

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
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = Component
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit

    def get_name(self, obj):
        return obj.ingredient.name


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = ComponentSerializer(many=True, source='components')
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
            'image',
            'name',
            'text',
            'cooking_time'
        )
        extra_kwargs = {
            'text': {'required': True},
            'cooking_time': {'required': True},
            'ingredients': {'required': True},
            'tags': {'required': True},
            'image': {'required': True},
            'is_favorited': {'required': True},
        }

    def get_is_favorited(self, obj):

        if self.context['request'].user.is_anonymous:
            return False

        return Favorite.objects.filter(
            user=self.context['request'].user,
            recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):

        if self.context['request'].user.is_anonymous:
            return False

        return ShoppingList.objects.filter(
            user=self.context['request'].user,
            recipe=obj).exists()


class UserRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        extra_kwargs = {
            'id': {'required': True},
            'cooking_time': {'required': True},
            'image': {'required': True},
        }


class UserFollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = UserRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        return obj.follow.filter(user=self.context['user']).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class ComponentSerializerCreate(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = Component
        fields = (
            'id',
            'amount',
        )
        extra_kwargs = {
            'amount': {'validators': []},
        }

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Количество ингредиента должно быть '
                'целым числом и не менее 1!'
            )
        return value

    # def validate_id(self, value):
    #     set_id = set()
    #     for item in self.context['request']._full_data['ingredients']:
    #         if (item['id'] in set_id) and (item['id'] == value.id):
    #             raise serializers.ValidationError(
    #                 'Ингредиенты в рецепте должны быть уникальны.')
    #         set_id.add(item['id'])
    #     return value


class RecipeSerializerCreate(serializers.ModelSerializer):
    ingredients = ComponentSerializerCreate(many=True, source='components')
    image = Base64ImageField(max_length=None, use_url=True)

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
            'cooking_time': {'required': True,
                             'validators': []},
            'ingredients': {'required': True},
            'tags': {'required': True},
            'image': {'required': True},
        }

    def validate_cooking_time(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Время приготовления должно быть '
                'целым числом и не менее 1 минуты!'
            )
        return value

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

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.ingredients.clear()
        instance.tags.clear()

        self.add_tags_and_components(instance, ingredients, tags)

        instance.save()
        return instance

    def validate_ingredients(self, value):
        if len(value) == 0:
            raise serializers.ValidationError(
                'Должен быть хоть один ингредиент.')
        set_id = set()
        for item in value:
            if item['ingredient'].id in set_id:
                raise serializers.ValidationError(
                    'Ингредиенты в рецепте должны быть уникальны.')
            set_id.add(item['ingredient'].id)
        return value

    def validate(self, data):
        if self.instance is None:
            return data
        if self.context['request'].user != self.instance.author:
            raise serializers.ValidationError('Нельзя изменить чужой рецепт!')
        return data

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
