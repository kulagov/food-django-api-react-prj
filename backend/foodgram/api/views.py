import json

import reportlab

from django.db import models
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .models import Component, Favorite, Ingredient, Recipe, ShoppingList, Tag
from .serializers import (
    ComponentSerializer, IngredientSerializer, RecipeSerializer,
    RecipeSerializerCreate, ShopAndFavoriteSerializer, TagSerializer,
)


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

    @action(detail=False)
    def download_shopping_cart(self, request):
        shop_list_user = ShoppingList.objects.filter(user=request.user)
        shop_list_amount = {}
        shop_list_name = {}
        for shop_item in shop_list_user:
            components = Component.objects.filter(recipe=shop_item.recipe)
            for comp_item in components:
                ingredient_item = comp_item.ingredient
                amount_item = comp_item.amount
                if ingredient_item.id in shop_list_amount.keys():
                    shop_list_amount[ingredient_item.id] = (
                        shop_list_amount[ingredient_item.id] + amount_item)
                else:
                    shop_list_amount[ingredient_item.id] = amount_item
                    shop_list_name[ingredient_item.id] = ingredient_item

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="somefilename.pdf"')

        canvas_blank = canvas.Canvas(response)
        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
        canvas_blank.setFont('FreeSans', 14)

        row = 800
        for ingredient_list in shop_list_amount:
            canvas_blank.drawString(
                100,
                row,
                f'{shop_list_name[ingredient_list]} - '
                f'{shop_list_amount[ingredient_list]}')
            row -= 20

        canvas_blank.showPage()
        canvas_blank.save()
        return response

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
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


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
