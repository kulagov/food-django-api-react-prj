from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import Ingredient


class IngredientSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')
