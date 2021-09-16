from re import I
from django.shortcuts import render
from rest_framework import viewsets

from .models import Ingredient
from .serializers import IngredientSerialiser


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerialiser
