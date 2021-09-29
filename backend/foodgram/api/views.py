import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .filters import IngredientsFilter, RecipesFilter
from .models import Component, Favorite, Ingredient, Recipe, ShoppingList, Tag
from .serializers import (
    ComponentSerializer, IngredientSerializer, RecipeSerializer,
    RecipeSerializerCreate, ShopAndFavoriteSerializer, TagSerializer,
)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = RecipeSerializer
    filterset_class = RecipesFilter
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in ['update', 'create']:
            return RecipeSerializerCreate
        return RecipeSerializer

    @action(detail=False)
    def download_shopping_cart(self, request):
        shop_list = list(
            request.user.shoppinglist.values_list('recipe__components'))
        for _ in range(0, len(shop_list)):
            shop_list[_] = shop_list[_][0]
        components = Component.objects.in_bulk(shop_list)
        shop_list_amount = {}
        shop_list_name = {}
        for comp_obj in components.values():
            ingredient_item = comp_obj.ingredient
            amount_item = comp_obj.amount
            if ingredient_item.id in shop_list_amount:
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
        canvas_blank.setFont('FreeSans', 18)

        row = 800
        canvas_blank.drawString(
            100,
            row,
            'Список покупок:')
        row -= 40

        canvas_blank.setFont('FreeSans', 14)
        item = 1
        for ingredient_list in shop_list_amount:
            ingredient_item = shop_list_name[ingredient_list].__str__()
            ingredient_item_cap = ingredient_item.capitalize()
            ammount_item = shop_list_amount[ingredient_list]
            canvas_blank.drawString(
                100,
                row,
                f'{item}. '
                f'{ingredient_item_cap} - '
                f'{ammount_item}')
            row -= 20
            item += 1

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
            get_object_or_404(
                ShoppingList,
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
            get_object_or_404(
                Favorite,
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
    filterset_class = IngredientsFilter
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = None


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
