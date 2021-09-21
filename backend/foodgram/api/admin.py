from django.contrib import admin
from django.db import models

from .models import Ingredient, Recipe, Tag, Component, ShoppingList


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name', )
    list_filter = ('measurement_unit', )


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    list_filter = ('name', 'color', 'slug')


class ComponentInline(admin.TabularInline):
    model = Component


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ('author', 'name', 'tags')
    inlines = [ComponentInline, ]


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_filter = ('user', 'recipe')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
