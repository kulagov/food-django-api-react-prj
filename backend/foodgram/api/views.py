import json

from rest_framework import filters, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Ingredient, Tag
from .serializers import IngredientSerializer, TagSerializer


class TagViewSet(viewsets.ModelViewSet):
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
            print(ingredients_data['name'])
    print('___ end load data ___')
    queryset = Ingredient.objects.all()
    serializer = IngredientSerializer(queryset, many=True)
    return Response(serializer.data)

