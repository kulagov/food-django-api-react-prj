import django_filters

from .models import Ingredient, Recipe


class IngredientsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ['name', ]


class RecipesFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(
        field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ['author', 'tags']
