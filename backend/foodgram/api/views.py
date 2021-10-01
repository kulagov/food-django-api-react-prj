from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.filters import IngredientsFilter, RecipesFilter
from api.models import (
    Component, Favorite, Ingredient, Recipe, ShoppingList, Tag,
)
from api.paginations import PageLimitPagination
from api.serializers import (
    ComponentSerializer, IngredientSerializer, RecipeSerializer,
    RecipeSerializerCreate, ShopAndFavoriteSerializer, TagSerializer,
)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = RecipeSerializer
    filterset_class = RecipesFilter
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = PageLimitPagination

    def get_serializer_class(self):
        if self.action in ['update', 'create']:
            return RecipeSerializerCreate
        return RecipeSerializer

    @action(detail=False)
    def download_shopping_cart(self, request):
        shop_list = list(
            request.user.shoppinglist.values_list('recipe__components'))
        for shop_list_item in range(0, len(shop_list)):
            shop_list[shop_list_item] = shop_list[shop_list_item][0]
        components = Component.objects.in_bulk(shop_list)

        shop_list_dict = {}

        for comp_obj in components.values():
            ingredient_item = comp_obj.ingredient
            amount_item = comp_obj.amount
            if ingredient_item.id in shop_list_dict:
                shop_list_dict[ingredient_item.id] = (
                    shop_list_dict[ingredient_item.id][0],
                    shop_list_dict[ingredient_item.id][1] + amount_item
                )
            else:
                shop_list_dict[ingredient_item.id] = (
                    ingredient_item.__str__(),
                    amount_item)

        sorted_list = dict(sorted(
            shop_list_dict.items(), key=lambda x: x[1][0]))

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

        for ingredient_list in sorted_list:
            ingredient_item, amount_item = sorted_list[ingredient_list]
            ingredient_item_cap = ingredient_item.capitalize()
            canvas_blank.drawString(
                100,
                row,
                f'{item}. '
                f'{ingredient_item_cap} - '
                f'{amount_item}')
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
