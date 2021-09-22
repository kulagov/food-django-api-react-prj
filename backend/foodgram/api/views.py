import json

from django.db import models
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .models import Component, Favorite, Ingredient, Recipe, ShoppingList, Tag
from .serializers import (ComponentSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeSerializerCreate,
                          ShopAndFavoriteSerializer, TagSerializer)


class ListDeleteViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        # mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    pass


# class RecipeViewSet(ListDeleteViewSet)
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_serializer_class(self):
        if self.action in ['update', 'create']:
            return RecipeSerializerCreate
        return RecipeSerializer

    @action(methods=['get', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None):
        if request.method == 'GET':
            ShoppingList.objects.get_or_create(
                user=request.user,
                recipe=self.get_object())

        serializer = ShopAndFavoriteSerializer(self.get_object())

        flag = ShoppingList.objects.filter(user=request.user,
                                           recipe=self.get_object()).exists()
        if (request.method == 'DELETE' and flag):
            ShoppingList.objects.get(
                user=request.user,
                recipe=self.get_object()
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.data)

    @action(methods=['get', 'delete'], detail=True)
    def favorite(self, request, pk=None):
        if request.method == 'GET':
            Favorite.objects.get_or_create(
                user=request.user,
                recipe=self.get_object())

        serializer = ShopAndFavoriteSerializer(self.get_object())

        flag = Favorite.objects.filter(user=request.user,
                                       recipe=self.get_object()).exists()
        if (request.method == 'DELETE' and flag):
            Favorite.objects.get(
                user=request.user,
                recipe=self.get_object()
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


@api_view(['GET', 'POST'])
def loaddata(request):
    print('___ start load data ___')
    with open('../../data/ingredients.json', encoding='utf-8') as data_file:
        json_data = json.loads(data_file.read())

        for ingredients_data in json_data:
            Ingredient.objects.get_or_create(
                name=ingredients_data['name'],
                measurement_unit=ingredients_data['measurement_unit']
            )
            # print(ingredients_data['name'])
    print('___ end load data ___')
    queryset = Ingredient.objects.all()
    serializer = IngredientSerializer(queryset, many=True)
    return Response(serializer.data)


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
