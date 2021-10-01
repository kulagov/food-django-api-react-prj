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
    is_favorited = django_filters.BooleanFilter(
        field_name='is_favorited',
        method='filter_is_favorited')
    is_in_shopping_cart = django_filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favlist__user=self.request.user)
        return queryset.exclude(favlist__user=self.request.user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shoppinglist__user=self.request.user)
        return queryset.exclude(shoppinglist__user=self.request.user)
