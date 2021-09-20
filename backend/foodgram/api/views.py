import json

from rest_framework import filters, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Component, Ingredient, Recipe, Tag
from .serializers import (ComponentSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeSerializerCreate,
                          TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_serializer_class(self):
        if self.action in ['update', 'create']:
            return RecipeSerializerCreate
        return RecipeSerializer


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

